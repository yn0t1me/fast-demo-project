# app/api/v1/heroes_route.py
from loguru import logger
from fastapi import APIRouter, Depends, status, Query # 👈 新增 Query
from sqlalchemy.ext.asyncio import AsyncSession

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


@router.get("", response_model=HeroListResponse)
async def list_heroes(
    # --- 使用 Query 定义更丰富的查询参数 ---
    search: str | None = Query(None, description="按名称、别名、能力进行模糊搜索"),
    order_by: str = Query("id", description="排序字段：name, alias, id"),
    direction: str = Query("asc", description="排序方向", regex="^(asc|desc)$"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(10, ge=1, le=100, description="每页数量"),
    # --- 依赖注入不变 ---
    service: HeroService = Depends(get_hero_service),
) -> HeroListResponse:
    try:
        # 1. 计算 offset
        offset = (page - 1) * limit

        # 2. 从服务层获取数据
        total, heroes = await service.get_heroes(
            search=search,
            order_by=order_by,
            direction=direction,
            limit=limit,
            offset=offset,
        )

        # 3. 计算分页信息
        total_pages = (total + limit - 1) // limit

        # 4. 组装最终的返回对象
        return HeroListResponse(
            data=heroes,
            pagination=Pagination(
                currentPage=page,
                totalPages=total_pages,
                totalItems=total,
                limit=limit,
                hasMore=page < total_pages,
                previousPage=page - 1 if page > 1 else None,
                nextPage=page + 1 if page < total_pages else None,
            ),
            sort=Sort(field=order_by, direction=direction),
            filters=Filters(search=search),
        )
    except Exception as e:
        logger.error(f"Failed to fetch heroes: {e}")
        raise


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