# app/domains/heroes/heroes_repository.py
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc, asc # 👈 新增导入

from app.core.exceptions import AlreadyExistsException, NotFoundException
from app.models.heroes import Hero
from app.schemas.heroes import HeroCreate, HeroUpdate


class HeroRepository:
    """Repository for handling hero database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, hero_data: HeroCreate) -> Hero:
        """Create a new hero."""
        hero = Hero(**hero_data.model_dump())
        try:
            self.session.add(hero)
            await self.session.commit()
            await self.session.refresh(hero)
            return hero
        except IntegrityError:
            await self.session.rollback()
            raise AlreadyExistsException(
                f"Hero with alias {hero_data.alias} already exists"
            )

    async def get_by_id(self, hero_id: int) -> Hero:
        """Fetch a hero by id."""
        hero = await self.session.get(Hero, hero_id)
        if not hero:
            raise NotFoundException(f"Hero with id {hero_id} not found")
        return hero

    # 👇 更新 get_all 方法
    async def get_all(
        self,
        *,
        search: str | None = None,
        order_by: str = "id",
        direction: str = "asc",
        limit: int = 10,
        offset: int = 0,
    ) -> tuple[int, list[Hero]]:
        query = select(Hero)

        # 1. 搜索/过滤逻辑
        if search:
            query = query.where(
                or_(
                    Hero.name.ilike(f"%{search}%"),
                    Hero.alias.ilike(f"%{search}%"),
                    Hero.powers.ilike(f"%{search}%"), # 别忘了我们新增的 powers 字段
                )
            )

        # 2. 排序逻辑
        # 使用 getattr 安全地获取排序字段，找不到就用 id
        order_column = getattr(Hero, order_by, Hero.id)
        query = query.order_by(desc(order_column) if direction == "desc" else asc(order_column))

        # 3. 获取总数 (分页前)
        # 先构建一个只查 count 的查询
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.session.scalar(count_query)) or 0

        # 4. 分页获取数据
        paginated_query = query.offset(offset).limit(limit)
        items = list(await self.session.scalars(paginated_query))
      
        return total, items

    async def update(self, hero_data: HeroUpdate, hero_id: int) -> Hero:
        """Update an existing hero."""
        hero = await self.get_by_id(hero_id) # 复用了 get_by_id 逻辑

        update_data = hero_data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields to update") # 这是一个标准的ValueError
          
        for key, value in update_data.items():
            setattr(hero, key, value)
          
        await self.session.commit()
        await self.session.refresh(hero)
        return hero

    async def delete(self, hero_id: int) -> None:
        """Delete a hero."""
        hero = await self.get_by_id(hero_id) # 复用了 get_by_id 逻辑

        await self.session.delete(hero)
        await self.session.commit()