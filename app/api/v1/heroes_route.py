# app/api/v1/heroes_route.py
from loguru import logger
from fastapi import APIRouter, Depends, status, Query # 👈 新增 Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, Params

from app.core.database import get_db
from app.domains.heroes.heroes_repository import HeroRepository
from app.domains.heroes.heroes_services import HeroService
from app.schemas.heroes import HeroCreate, HeroUpdate, HeroResponse, HeroStoryResponse, HeroListResponse, Pagination, Sort, Filters


router = APIRouter(prefix="/heroes", tags=["Heroes"])


def get_hero_service(session: AsyncSession = Depends(get_db)) -> HeroService:
    """Dependency for getting HeroService instance."""
    repository = HeroRepository(session)
    return HeroService(repository)


@router.post("", response_model=HeroResponse, status_code=status.HTTP_201_CREATED)
async def create_hero(
    data: HeroCreate, service: HeroService = Depends(get_hero_service)
) -> HeroResponse:
    """Create new hero."""
    try:
        created_hero = await service.create_hero(data=data)
        logger.info(f"Created hero with id: {created_hero.id}")
        return created_hero
    except Exception as e:
        logger.error(f"Failed to create hero: {e}")
        raise


@router.get("", response_model=Page[HeroResponse])
async def list_heroes(
    # --- 使用 Query 定义更丰富的查询参数 ---
    search: str | None = Query(None, description="按名称、别名、能力进行模糊搜索"),
    # 👇 Query 现在接收一个字符串列表
    order_by: list[str] | None = Query(
        None,
        description="排序字段列表, 如 '-name,alias'。'-'前缀表示降序, 默认升序。",
        example=["-name", "alias"], # 在文档中提供清晰的示例
    ),
    # 👇 分页参数由这一个依赖项搞定
    params: Params = Depends(),
    # --- 依赖注入不变 ---
    service: HeroService = Depends(get_hero_service),
) -> Page[HeroResponse]:
    # 直接调用服务层，几乎没有额外逻辑
    return await service.get_heroes(
        search=search,
        order_by=order_by,
        params=params,
    )


@router.get("/{hero_id}", response_model=HeroResponse)
async def get_hero(
    hero_id: int,
    service: HeroService = Depends(get_hero_service),
) -> HeroResponse:
    """Get hero by id."""
    try:
        hero = await service.get_hero(hero_id=hero_id)
        logger.info(f"Retrieved hero {hero_id}")
        return hero
    except Exception as e:
        logger.error(f"Failed to get hero {hero_id}: {e}")
        raise


@router.patch("/{hero_id}", response_model=HeroResponse, status_code=status.HTTP_200_OK)
async def update_hero(
    data: HeroUpdate,
    hero_id: int,
    service: HeroService = Depends(get_hero_service),
) -> HeroResponse:
    """Update hero."""
    try:
        updated_hero = await service.update_hero(data=data, hero_id=hero_id)
        logger.info(f"Updated hero {hero_id}")
        return updated_hero
    except Exception as e:
        logger.error(f"Failed to update hero {hero_id}: {e}")
        raise


@router.delete("/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hero(
    hero_id: int,
    service: HeroService = Depends(get_hero_service),
) -> None:
    """Delete hero."""
    try:
        await service.delete_hero(hero_id=hero_id)
        logger.info(f"Deleted hero {hero_id}")
    except Exception as e:
        logger.error(f"Failed to delete hero {hero_id}: {e}")
        raise
  
  
@router.get("/{hero_id}/story", response_model=HeroStoryResponse)
async def generate_hero_story(
    hero_id: int,
    service: HeroService = Depends(get_hero_service),
) -> HeroResponse:
    """Generate hero story."""
    try:
        story = await service.get_hero_with_story(hero_id=hero_id)
        logger.info(f"Generated story for hero {hero_id}")
        return story
    except Exception as e:
        logger.error(f"Failed to generate hero's story for hero_id={hero_id}: {e}")
        raise