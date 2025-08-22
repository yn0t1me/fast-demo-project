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