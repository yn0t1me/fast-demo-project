# app/schemas/heroes.py
from pydantic import BaseModel
from typing import Literal # 👈 确保导入 Literal


# 基础模型，定义了所有Hero共有的字段
class HeroBase(BaseModel):
    name: str
    alias: str

# 创建Hero时，从请求体中读取的模型
class HeroCreate(HeroBase):
    pass

# 更新Hero时，允许部分字段可选
class HeroUpdate(BaseModel):
    name: str | None = None
    alias: str | None = None

# 从数据库读取并返回给客户端的模型
class HeroResponse(HeroBase):
    id: int
  
    class Config:
        from_attributes = True  # 关键配置！允许模型从ORM对象的属性中读取数据

# 新增一个用于返回带故事的英雄信息的模型
class HeroStoryResponse(HeroResponse):
    """
    继承自 HeroResponse，并增加一个 story 字段
    """
    story: str

# --- 新增的返回结构模型 ---

# 1. 分页信息模型
class Pagination(BaseModel):
    currentPage: int
    totalPages: int
    totalItems: int
    limit: int
    hasMore: bool
    previousPage: int | None # 可能没有上一页
    nextPage: int | None     # 可能没有下一页


# ----------------- 我们改造多条件排序的起点 -----------------
# 1. 新增一个用于描述单条排序规则的模型
class OrderByRule(BaseModel):
    field: str
    dir: Literal["asc", "desc"] = "asc" # 方向只能是 "asc" 或 "desc"

# 2. 修改 Sort 模型，使其包含一个规则列表
class Sort(BaseModel):
    fields: list[OrderByRule]

# ----------------- 我们改造多条件排序的终点 -----------------

# 3. 过滤信息模型
class Filters(BaseModel):
    search: str | None

# 4. 最终的、集大成的列表响应模型
class HeroListResponse(BaseModel):
    data: list[HeroResponse] # 数据本身是一个 HeroResponse 列表
    pagination: Pagination   # 嵌套 Pagination 模型
    sort: Sort               # 嵌套 Sort 模型
    filters: Filters           # 嵌套 Filters 模型