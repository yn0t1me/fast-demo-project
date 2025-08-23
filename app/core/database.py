# /fastapi-demo-project/app/core/database.py
from typing import Optional, AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from loguru import logger
from app.core.config import settings
# 导入统一的 Base 类
from app.models.base import Base

# --- 1. 全局变量定义 ---
_engine: Optional[AsyncEngine] = None
_SessionFactory: Optional[async_sessionmaker[AsyncSession]] = None

def get_engine() -> AsyncEngine:
    if _engine is None:
        raise RuntimeError("数据库引擎未初始化. 请先调用 setup_database_connection")
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    if _SessionFactory is None:
        raise RuntimeError("会话工厂未初始化. 请先调用 setup_database_connection")
    return _SessionFactory


# --- 2. 通用的数据库初始化和关闭函数 ---
# 这些函数现在是通用的，可以在任何需要初始化数据库的地方调用。
# 它们负责设置全局的 engine 和 SessionFactory。
async def setup_database_connection():
    """
    初始化全局的数据库引擎和会话工厂。
    这是一个通用的设置函数，可以在 FastAPI 启动时调用。
    """
    global _engine, _SessionFactory
    
    if _engine is not None:
        logger.info("数据库已初始化，跳过重复设置。")
        return
    
    logger.info("正在创建数据库引擎...")
    _engine = create_async_engine(
        # 从我们上一章的 settings 对象中读取计算生成的数据库连接字符串
        settings.DB.DATABASE_URL,
        pool_size=settings.DB.POOL_SIZE,
        max_overflow=settings.DB.MAX_OVERFLOW,
        pool_timeout=settings.DB.POOL_TIMEOUT,
        pool_recycle=settings.DB.POOL_RECYCLE,
        echo=settings.DB.ECHO,
        pool_pre_ping=True,
    )
    
    # SessionFactory 是一个"会话的工厂"，配置一次，随处使用
    _SessionFactory = async_sessionmaker(
        class_=AsyncSession, expire_on_commit=False, bind=_engine
    )
    
    logger.info("数据库引擎和会话工厂已成功创建。")

async def close_database_connection():
    """在应用关闭时，关闭全局的数据库引擎连接池。"""
    global _engine, _SessionFactory
    
    if _engine:
        await _engine.dispose()
        _engine = None
        _SessionFactory = None
        logger.info("数据库引擎连接池已关闭。")

# --- 3. 依赖注入魔法：获取会话 ---
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI 依赖注入函数，为每个请求提供一个独立的数据库会话。
    """
    if _SessionFactory is None:
        raise RuntimeError("数据库会话工厂未初始化。请确保在应用启动时调用了 setup_database_connection()。")
    
    # 从会话工厂创建一个新的会话
    async with _SessionFactory() as session:
        # 使用 yield 将会话提供给路径函数
        yield session
        # 当请求处理完成后，async with 会自动处理会话的关闭


# --- 4. 辅助工具：创建数据库表 ---
async def create_db_and_tables():
    """
    一个开发工具，用于在应用启动前创建所有定义的数据库表。
    注意：在生产环境中你可能需要更专业的迁移工具如 Alembic。
    """
    if not _engine:
        raise RuntimeError("数据库引擎未初始化。请确保在应用启动时调用了 setup_database_connection()。")
    async with _engine.begin() as conn:
        # 让 SQLAlchemy 根据所有继承了 Base 的模型类去创建表
        await conn.run_sync(Base.metadata.create_all)
        logger.info("数据库表已成功同步/创建。")