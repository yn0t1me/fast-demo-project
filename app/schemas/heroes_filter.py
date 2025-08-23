# app/schemas/heroes_filter.py
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from app.models.heroes import Hero

class HeroFilter(Filter):
    # 1. 定义查询参数
    search: str | None = Field(None, description="按 name/alias/powers 模糊搜索")
    order_by: list[str] = Field(
        [],
        description="排序字段，如 '-name,powers'", # 注意：库的默认行为是用逗号分隔
        json_schema_extra={"example": ["-name", "powers"]},
    )

    # 2. 保留我们的自定义排序增强逻辑
    def sort(self, query):
        # a. 首先，让父类的 sort 方法处理来自前端的 order_by 参数
        if self.ordering_values:
            query = super().sort(query)

        # b. 然后，追加我们自己的默认/固定排序规则
        if not any(v.lstrip("+-") == "name" for v in self.ordering_values):
            query = query.order_by(Hero.name.asc())
        query = query.order_by(Hero.id.asc())

        return query

    # 3. 配置元数据
    class Constants(Filter.Constants):
        model = Hero  # 指定此 Filter 关联的 SQLAlchemy 模型
        search_model_fields = ["name", "alias", "powers"] # 指定 `search` 参数应该搜索哪些字段