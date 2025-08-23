# app/schemas/heroes.py
from pydantic import BaseModel

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

# 2. 排序信息模型
class Sort(BaseModel):
    field: str
    direction: str # "asc" 或 "desc"

# 3. 过滤信息模型
class Filters(BaseModel):
    search: str | None

# 4. 最终的、集大成的列表响应模型
class HeroListResponse(BaseModel):
    data: list[HeroResponse] # 数据本身是一个 HeroResponse 列表
    pagination: Pagination   # 嵌套 Pagination 模型
    sort: Sort               # 嵌套 Sort 模型
    filters: Filters           # 嵌套 Filters 模型