# app/domains/heroes/heroes_services.py
from fastapi_pagination import Page, Params, paginate   # 👈 导入内存分页函数

from app.domains.heroes.heroes_repository import HeroRepository
from app.schemas.heroes import HeroCreate, HeroUpdate, HeroResponse, HeroStoryResponse

class HeroService:
    def __init__(self, repository: HeroRepository):
        """Service layer for hero operations."""
        self.repository = repository

    async def create_hero(self, data: HeroCreate) -> HeroResponse:
        new_hero = await self.repository.create(data)
        return HeroResponse.model_validate(new_hero)

    async def get_hero(self, hero_id: int) -> HeroResponse:
        hero = await self.repository.get_by_id(hero_id)
        return HeroResponse.model_validate(hero)

    # 👇 更新 get_heroes 方法
    async def get_heroes(
        self,
        *,
        search: str | None,
        order_by: list[str] | None = None,
        params: Params,  # 👈 接收来自 fastapi-pagination 的分页参数
    ) -> Page[HeroResponse]: # 👈 返回值是 Page[HeroResponse]
        # 1. 从仓库获取 **所有** 过滤和排序后的数据
        heroes_orm_list = await self.repository.get_all(
            search=search,
            order_by=order_by,
            # 注意：这里不传递 limit 和 offset
        )
      
        # 2. 将 ORM 对象列表转换为 Pydantic 模型列表
        heroes_dto_list = [HeroResponse.model_validate(h) for h in heroes_orm_list]
      
        # 3. 使用 paginate 函数对内存中的列表进行分页
        return paginate(heroes_dto_list, params)

    async def update_hero(self, data: HeroUpdate, hero_id: int) -> HeroResponse:
        hero = await self.repository.update(data, hero_id)
        return HeroResponse.model_validate(hero)

    async def delete_hero(self, hero_id: int) -> None:
        await self.repository.delete(hero_id)

    async def get_hero_with_story(self, hero_id: int) -> HeroStoryResponse:
        """
        获取英雄信息，并动态生成一段背景故事。
        这个方法完美展示了服务层的业务逻辑处理能力。
        """
        # 1. 调用仓库层，获取最原始的数据库数据
        hero_orm = await self.repository.get_by_id(hero_id) 
 
        # 2. 在服务层中应用“业务逻辑”
        # 这里的逻辑是：根据英雄的名字和别名，虚构一段故事
        story_template = (
            f"在繁华的都市背后，流传着一个传说……那就是“{hero_orm.alias}”！"
            f"很少有人知道，这位在暗夜中守护光明的英雄，其真实身份是 {hero_orm.name}。"
            f"每一个被TA拯救的人，都会在心中默默记下这个名字。"
        ) 

        # 3. 构造并返回一个新的、带有附加信息的数据模型
        return HeroStoryResponse(
            id=hero_orm.id,
            name=hero_orm.name,
            alias=hero_orm.alias,
            story=story_template,
        )