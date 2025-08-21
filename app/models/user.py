# app/models/user.py
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base # 从同级目录的 base.py 导入 Base
from app.models.mixin import DateTimeMixin  # 导入 Mixin


class User(Base, DateTimeMixin):  # 同时继承，顺序不重要
    __tablename__ = "users" # 数据库中的表名
    
    # Mapped[...] 是 SQLAlchemy 2.0 的核心语法，用于类型注解
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(64), index=True, unique=True, nullable=False
    )
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))

    # 一个好的习惯：定义 __repr__ 方法，方便调试时打印对象信息
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"