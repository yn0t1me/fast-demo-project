# /fastapi-demo-project/app/main.py
from loguru import logger
from fastapi import Depends, FastAPI, Response
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
# 从 config 模块导入 get_settings 函数和 get_project_version 函数
from app.core.config import Settings, get_settings, get_project_version, settings
# 从 core.database 模块导入 setup_database_connection 和 close_database_connection 函数
from app.db.session import (
    setup_database_connection,
    close_database_connection,
    create_db_and_tables,
    get_db,
)
# 导入所有模型，确保它们被注册到 Base.metadata 中
import app.models

# 使用 lifespan 管理应用生命周期事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时执行
    get_settings()  # 应用启动时触发配置加载和缓存
    await setup_database_connection()
    # [可选] 在开发时创建表
    if settings.ENVIRONMENT == "dev":
        await create_db_and_tables()

    logger.info("🚀 应用启动，数据库已连接。")
    yield
    # 应用关闭时执行
    await close_database_connection()
    logger.info("应用关闭，数据库连接已释放。")



app = FastAPI(
    title=settings.APP_NAME,
    description="这是一个 FastAPI 演示项目",
    # 动态从 pyproject.toml 读取版本号
    version=get_project_version(),
    lifespan=lifespan

)

@app.get("/")
def read_root(
    # 通过 Depends(get_settings) 将配置实例注入到路由函数中
    # FastAPI 会在每次请求时自动调用 get_settings()，由于缓存的存在，每次调用会直接返回缓存的实例，性能开销极小
    settings: Settings = Depends(get_settings)
):
    """
    一个示例端点，演示如何访问配置。
    """
    return {
        "message": f"Hello from the {settings.APP_NAME}!",
        "environment": settings.ENVIRONMENT,
        "debug_mode": settings.DEBUG,
        # 演示如何访问嵌套的配置项
        "database_host": settings.DB.HOST,
        # 演示如何使用在模型中动态计算的属性
        "database_url_hidden_password": settings.DB.DATABASE_URL.replace(
            settings.DB.PASSWORD, "****"
        ),
        "app_version": get_project_version()
    }

   
@app.get("/db-check")
async def db_check(db: AsyncSession = Depends(get_db)):
    """
    一个简单的端点，用于检查数据库连接是否正常工作。
    """
    try:
        # 执行一个简单的查询来验证连接
        result = await db.execute(text("SELECT 1"))
        if result.scalar_one() == 1:
            return {"status": "ok", "message": "数据库连接成功！"}
    except Exception as e:
        return {"status": "error", "message": f"数据库连接失败: {e}"}