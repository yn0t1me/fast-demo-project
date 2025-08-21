# app/models/base.py
from sqlalchemy.orm import DeclarativeBase
# 定义所有 ORM 模型的基础类
class Base(DeclarativeBase):
    pass