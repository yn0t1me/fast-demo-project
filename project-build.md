# FastAPI 项目初始化

本文档基于 FastAPI 项目实战指南，详细记录从项目初始化到部署的完整流程。

## 项目初始化

### 创建项目与 Git 初始化

#### 创建项目目录

```bash
mkdir fastapi-demo-project
cd fastapi-demo-project
```

#### Git 初始化

```bash
git init
```

#### 连接到 GitHub

1. 在 GitHub 创建新的空仓库（不要勾选生成 README 或 .gitignore）
2. 复制仓库的 SSH 地址
3. 关联本地仓库与远程仓库：

```bash
# 将下面的地址换成你自己的仓库地址
git remote add origin git@github.com:username/fastapi-demo-project.git
# 验证是否连接成功
git remote -v
```

#### 创建初始提交并推送

```bash
# 创建 README 文件
echo "# FastAPI Demo Project" > README.md
# 将文件添加到暂存区
git add README.md
# 提交更改
git commit -m "Initial commit"
# 重命名默认分支为 main
git branch -M main
# 推送到 GitHub
git push -u origin main
```

### 使用 UV 配置环境

#### 创建功能分支

```bash
git checkout -b feature/initial-setup
```

#### 初始化 UV 项目

```bash
uv init
```

这个命令会自动生成：
- `pyproject.toml`
- `uv.lock`
- `main.py`

#### 创建并激活虚拟环境

```bash
uv venv
```

UV 会创建一个名为 `.venv` 的文件夹，存放项目隔离的 Python 环境。

#### 安装 FastAPI

```bash
uv add "fastapi[standard]"
```

这个命令会：
- 安装 FastAPI 及其标准依赖
- 自动将依赖记录到 `pyproject.toml` 文件中

### 编写第一个健康检查接口

#### 整理目录结构

1. 在根目录创建 `app` 文件夹
2. 将 `main.py` 移动到 `app/` 目录下

#### 编写接口代码

在 `app/main.py` 中写入以下代码：

```python
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}
```

#### 运行项目

```bash
uv run fastapi dev
```

`dev` 参数会自动开启 `--reload` 热重载功能，适合开发阶段使用。

#### 验证接口

- 浏览器访问：`http://127.0.0.1:8000/health`
- 或使用 curl 命令：

```bash
curl http://127.0.0.1:8000/health
```

预期返回：`{"status":"ok"}`

### 提交功能并合并到主分支

#### 配置 .gitignore

在项目根目录创建 `.gitignore` 文件：

```gitignore
# Virtual environments
.venv/
.env

# Python-generated files
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info
```

#### 提交功能分支

```bash
# 将所有改动添加到暂存区
git add .
# 创建描述性提交
git commit -m "feat: add initial project setup with health check"
# 推送功能分支到 GitHub
git push -u origin feature/initial-setup
```

#### 合并回主分支

```bash
# 切换回主分支
git checkout main
# 合并功能分支
git merge feature/initial-setup
# 推送更新到远程主分支
git push origin main
# 删除本地功能分支（可选）
git branch -d feature/initial-setup
# 删除远程功能分支（可选）
git push origin --delete feature/initial-setup
```

### 项目结构

完成以上步骤后，项目结构如下：

```
fastapi-demo-project/
├── .gitignore
├── .python-version
├── README.md
├── app/
│   └── main.py
├── pyproject.toml
└── uv.lock
```

## 构建环境感知的动态配置系统

基于 pydantic-settings 库构建专业、健壮且可扩展的配置系统，实现环境分离和性能优化。

1. 结构化配置：使用嵌套的 Pydantic 模型来组织配置项，让结构更清晰。
2. 环境分离：通过环境变量动态加载不同的配置文件（如 .env.dev, .env.prod）。
3. 性能优化：使用 @lru_cache 缓存配置，确保高性能和全局一致性。
4. 动态版本控制：从 pyproject.toml 自动读取项目版本号，保持 API 文档同步。
5. 命名空间安全：为环境变量添加前缀，避免与其他应用冲突。

利用 Pydantic 的类型检查能力来验证从环境变量或 .env 文件加载的配置。

我们将使用 DEMO_ 作为所有环境变量的前缀，这是一个非常好的习惯，可以防止你的应用配置与服务器上其他应用的配置发生冲突。

### 安装配置依赖

```bash
uv add pydantic-settings
```

### 创建环境配置文件

#### 创建配置模板文件

在项目根目录创建 `.env.sample` 文件：

```bash
# /.env.sample
# 这是一个配置模板文件。请根据此模板创建你自己的 .env.dev 或 .env.prod 文件。

# 应用配置
DEMO_DEBUG=True
DEMO_APP_NAME="FastAPI Demo Project (Dev)"

# 数据库配置
DEMO_DB_HOST=localhost
DEMO_DB_PORT=5432
DEMO_DB_USER=postgres
DEMO_DB_PASSWORD=postgres
DEMO_DB_DB=tutorial
```

#### 创建开发环境配置

创建 `.env.dev` 文件：

```bash
# /.env.dev
# 开发环境专属配置

# 应用配置
DEMO_DEBUG=True
DEMO_APP_NAME="FastAPI Demo Project (Dev)"

# 数据库配置
DEMO_DB_HOST=localhost
DEMO_DB_PORT=5432
DEMO_DB_USER=postgres
DEMO_DB_PASSWORD=postgres
DEMO_DB_DB=tutorial
```

#### 创建生产环境配置

创建 `.env.prod` 文件：

```bash
# /.env.prod
# 生产环境专属配置

# 应用配置
DEMO_DEBUG=False
DEMO_APP_NAME="FastAPI Demo Project"

# 数据库配置 (通常会连接到不同的生产数据库)
DEMO_DB_HOST=prod.db.internal.cloud
DEMO_DB_PORT=5432
DEMO_DB_USER=project_prod_user
DEMO_DB_PASSWORD=a_very_secret_production_password
DEMO_DB_DB=prod_db
```

### 更新 .gitignore

更新 `.gitignore` 文件，忽略真实的环境配置文件：

```gitignore
# Virtual environments
.venv/
.env.*  # 忽略所有以 .env. 开头的文件
!.env.sample # 但不要忽略 .env.sample 文件

# Python-generated files
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info
```

### 创建配置系统

#### 创建 core 目录

```bash
mkdir -p app/core
touch app/core/__init__.py
```

#### 创建配置文件

在 `app/core/config.py` 中实现配置系统：

```python
# /fastapi-demo-project/app/core/config.py
import os
from functools import lru_cache
from typing import Literal

# 使用 Python 3.8+ 内置的 importlib.metadata
from importlib import metadata

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


# --- 动态版本号获取 ---
def get_project_version() -> str:
    """从 pyproject.toml 文件中动态读取项目版本号。"""
    try:
        # "fastapi-demo-project" 必须与你在 pyproject.toml 中定义的 [project] name 完全匹配
        return metadata.version("fastapi-demo-project")
    except metadata.PackageNotFoundError:
        # 如果包没有被 "安装" (例如，在 Docker 构建的早期阶段或非标准环境中)
        # 提供一个合理的回退值。
        return "0.1.0-dev"


# --- 嵌套配置模型 ---
# 这是一个最佳实践，它将相关的配置分组，使结构更清晰。


class DatabaseSettings(BaseSettings):
    """数据库相关配置"""

    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "postgres"
    PASSWORD: str = "postgres"
    DB: str = "tutorial"

    # 使用 @computed_field，可以在模型内部根据其他字段动态生成新字段
    # 这比在模型外部手动拼接字符串要优雅得多。
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """生成异步 PostgreSQL 连接字符串。"""
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"

    # model_config 的设置在这里同样适用，用于 Pydantic 如何加载这些设置
    model_config = SettingsConfigDict(env_prefix="DEMO_DB_")


class Settings(BaseSettings):
    """主配置类，汇集所有配置项。"""

    # 环境配置: 'dev' 或 'prod'
    # Literal 类型确保了 ENVIRONMENT 只能是指定的值之一，增加了类型安全
    ENVIRONMENT: Literal["dev", "prod"] = "dev"

    DEBUG: bool = False
    APP_NAME: str = "FastAPI Demo Project"
    
    # --- 嵌套配置 ---
    # 将 DatabaseSettings 作为主 Settings 的一个字段。
    # Pydantic 会自动处理带有 'DEMO_DB_' 前缀的环境变量，并填充到这个模型中。
    DB: DatabaseSettings = DatabaseSettings()

    # Pydantic-settings 的核心配置
    model_config = SettingsConfigDict(
        # 从 .env 文件加载环境变量,这里不写，放到动态加载了
        env_file_encoding="utf-8",
        # 为顶层配置项设置前缀
        env_prefix="DEMO_",
        # 允许大小写不敏感的环境变量
        case_sensitive=False,
    )


# --- 缓存与依赖注入 ---
# 这是整个配置系统的关键入口点。
@lru_cache
def get_settings() -> Settings:
    """
    创建并返回一个配置实例。

    使用 @lru_cache 装饰器实现以下目标：
    1. 性能: 配置只在应用启动时被加载和解析一次，而不是在每个请求中。
    2. 一致性 (单例): 应用的任何部分调用此函数都将获得完全相同的配置对象实例。

    这意味着，如果你在应用运行时更改了 .env 文件，你需要重启应用才能使更改生效。
    """
    print("正在加载配置...") # 这条消息只会在应用首次启动时打印一次

    # 根据 ENVIRONMENT 环境变量来决定加载哪个 .env 文件
    # 这是一个非常灵活的模式
    env = os.getenv("ENVIRONMENT", "dev")
    env_file = f".env.{env}"
    # 动态创建 Settings 实例，会覆盖 SettingsConfigDict 中的 env_file 设置
    settings = Settings(_env_file=env_file)  # type: ignore
    print(f"成功加载 '{env}' 环境配置 for {settings.APP_NAME}")
    return settings


# 在应用启动时就创建一个实例，方便在非 FastAPI 上下文中使用
settings = get_settings()
```

### 更新主应用文件

更新 `app/main.py` 以使用新的配置系统：

```python
# /fastapi-demo-project/app/main.py

from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager

# 从 config 模块导入 get_settings 函数和 get_project_version 函数
from app.core.config import Settings, get_settings, get_project_version

# Lifespan: 在应用启动时调用 get_settings，触发配置加载和缓存
@asynccontextmanager
async def lifespan(app: FastAPI):
    get_settings()  # 应用启动时触发配置加载和缓存
    yield  # 应用运行期间，保持配置缓存
    # 应用关闭时，这里可以添加清理资源的代码


# 获取配置实例
settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    # 动态从 pyproject.toml 读取版本号
    version=get_project_version(),
    lifespan=lifespan  # FastAPI 应用生命周期管理，应用启动时调用 lifespan 函数

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
```

指定lifespan，在 FastAPI 应用启动时自动调用 get_settings() ，触发配置系统的初始化和缓存机制，确保配置在应用启动阶段就被正确加载



### 运行不同环境

创建一个只包含 ENVIRONMENT 变量的文件，然后让 uv 加载它

#### 创建环境声明文件
为我们的每个环境创建一个小的"声明文件"。这个文件只用来告诉我们的应用它应该加载哪个主配置文件

创建 `env.dev` 文件：

```bash
ENVIRONMENT=dev
```

创建 `env.prod` 文件：

```bash
ENVIRONMENT=prod
```

#### 使用 uv run 运行
当你想以开发模式启动时，运行：
```bash
uv run --env-file env.dev -- fastapi dev
```
当你想以生产模式启动时，你运行：
```bash
uv run --env-file env.prod -- fastapi run
```

#### 工作原理
1. `uv run --env-file env.dev` 会读取 `env.dev` 文件，并将 `ENVIRONMENT=dev` 这个变量加载到运行环境中
2. 然后 uv 启动 Python 进程
3. 在你的 Python 代码中，`os.getenv("ENVIRONMENT", "dev")` 成功地读取到了 "dev"
4. 你的 `get_settings()` 工厂函数因此构造出路径 ".env.dev"
5. 最终 `Settings(_env_file=".env.dev")` 成功加载了正确的配置文件

#### 验证配置加载
启动应用后，访问 `http://127.0.0.1:8000/` 可以看到当前环境的配置信息，包括：
- 应用名称
- 环境类型（dev/prod）
- 调试模式状态
- 数据库主机信息
- 应用版本号

### 项目结构总览

完成配置系统后，最终的项目结构如下：

```
fastapi-demo-project/
├── .env.sample          # 配置模板文件
├── .env.dev             # 开发环境配置
├── .env.prod            # 生产环境配置
├── .gitignore           # Git 忽略文件
├── .python-version      # Python 版本声明
├── README.md            # 项目说明文档
├── app/                 # 应用主目录
│   ├── __init__.py
│   ├── core/            # 核心模块
│   │   ├── __init__.py
│   │   └── config.py    # 配置系统
│   └── main.py          # 主应用文件
├── docs/                # 文档目录
│   └── pydantic-settings-guide.md
├── env.dev              # 开发环境声明文件
├── env.prod             # 生产环境声明文件
├── project-build.md     # 项目构建文档
├── pyproject.toml       # 项目配置文件
└── uv.lock              # 依赖锁定文件
```

## 驾驭 SQLAlchemy 2.0，构建现代异步数据库连接

基于 SQLAlchemy 2.0 和异步 PostgreSQL 构建健壮、可复用的数据库连接层，并无缝整合进 FastAPI 的生命周期与依赖注入系统。


### 设计哲学：优秀的数据库连接层

一个优秀的数据库模块应该满足以下几点：

1. **全局唯一引擎 (Singleton Engine)**：数据库引擎是一个"重型"对象，它管理着底层的连接池。在整个应用生命周期中，我们只需要一个实例就够了，重复创建是对资源的极大浪费。
2. **按需会话 (Per-Request Session)**：每个独立的请求或任务都应该获取一个全新的、独立的数据库会话。用完后立即归还。这能有效避免数据串扰、并发问题，保证事务的隔离性。
3. **优雅启停 (Graceful Lifespan)**：数据库连接应该在应用启动时被建立，在应用关闭时被优雅地释放。绝不能在第一个用户请求进来时才手忙脚乱地去初始化。
4. **依赖注入 (Dependency Injection)**：在 FastAPI 中，我们希望能够像变魔术一样，在任何需要操作数据库的路径函数中，通过 Depends 轻松地拿到一个可用的会话。

### 扩展数据库配置

首先，我们需要扩展配置系统以支持数据库连接池的相关参数。

更新 `app/core/config.py` 中的 `DatabaseSettings` 类：

```python
class DatabaseSettings(BaseSettings):
    """数据库相关配置"""

    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "postgres"
    PASSWORD: str = "postgres"
    DB: str = "tutorial"

    # 连接池配置
    POOL_SIZE: int = 10
    MAX_OVERFLOW: int = 20
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 3600
    ECHO: bool = False

    # 使用 @computed_field，可以在模型内部根据其他字段动态生成新字段
    # 这比在模型外部手动拼接字符串要优雅得多。
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """生成异步 PostgreSQL 连接字符串。"""
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"

    # model_config 的设置在这里同样适用，用于 Pydantic 如何加载这些设置
    model_config = SettingsConfigDict(env_prefix="DEMO_DB_")
```

### 安装数据库依赖

```bash
uv add sqlalchemy[asyncio] asyncpg loguru
```

这将安装：
- `sqlalchemy[asyncio]`：SQLAlchemy 2.0 异步支持
- `asyncpg`：高性能异步 PostgreSQL 驱动
- `loguru`：现代化的日志库

### 创建数据库连接模块

#### 创建数据库目录

```bash
mkdir -p app/db
touch app/db/__init__.py
```

#### 实现数据库会话管理

第 1 部分：我们定义了两个全局变量 _engine 和 _SessionFactory，它们是整个模块的核心。Base 是所有数据模型的基础，SQLAlchemy 会通过它追踪所有需要被映射到数据库的表。

第 2 部分：setup_database_connection 和 close_database_connection 是我们的“开关”。它们被设计为与 FastAPI 的**生命周期（lifespan）**事件完美集成。注意到我们是如何从 settings 对象中获取配置的吗？这正是上一章工作的成果！

第 3 部分：get_db 是真正的魔法所在！它是一个异步生成器 (AsyncGenerator)。FastAPI 的依赖注入系统知道如何处理它：当请求进来时，它会执行到 yield session，把 session 对象“注入”到你的路径函数中；当你的路径函数执行完毕后，它会回来继续执行 yield 后面的代码（在这里 async with 会自动关闭会话），完美实现了资源的申请与释放。

第 4 部分：create_db_and_tables 是一个方便的开发工具，我们可以在启动时调用它来确保所有表都已创建。

在 `app/db/session.py` 中实现数据库连接系统：

```python
# /fastapi-demo-project/app/db/session.py
from typing import Optional, AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase
from loguru import logger
from app.core.config import settings

# --- 1. 核心组件：全局引擎与会话工厂 ---
_engine: Optional[AsyncEngine] = None
_SessionFactory: Optional[async_sessionmaker[AsyncSession]] = None

# 基类，我们所有的 ORM 模型都需要继承它
class Base(DeclarativeBase):
    pass

# --- 2. 生命周期钩子：初始化与关闭 ---
async def setup_database_connection():
    """在应用启动时，初始化全局的数据库引擎和会话工厂。"""
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

```

### 更新应用生命周期管理

更新 `app/main.py` 以集成数据库连接管理：

```python
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
```

### 更新环境配置文件

更新 `.env.dev` 文件以包含数据库连接池配置：

```bash
# /.env.dev
# 开发环境专属配置

# 应用配置
DEMO_DEBUG=True
DEMO_APP_NAME="FastAPI Demo Project (Dev)"

# 数据库配置
DEMO_DB_HOST=localhost
DEMO_DB_PORT=5432
DEMO_DB_USER=postgres
DEMO_DB_PASSWORD=postgres
DEMO_DB_DB=tutorial

# 数据库连接池配置
DEMO_DB_POOL_SIZE=5
DEMO_DB_MAX_OVERFLOW=10
DEMO_DB_POOL_TIMEOUT=30
DEMO_DB_POOL_RECYCLE=3600
DEMO_DB_ECHO=True
```

### 测试数据库连接

#### 启动 PostgreSQL 数据库

如果你还没有 PostgreSQL 数据库，可以使用 Docker 快速启动一个：

```bash
docker run --name postgres-demo \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=tutorial \
  -p 5432:5432 \
  -d postgres:15
```

#### 运行应用并测试

```bash
# 启动开发服务器
uv run --env-file env.dev -- fastapi dev
```

访问以下端点进行测试：
- `http://127.0.0.1:8000/` - 查看应用基本信息
- `http://127.0.0.1:8000/db-check` - 测试数据库连接

### 核心特性总结

我们构建的数据库连接系统具有以下特性：

1. **单例引擎**：全局唯一的数据库引擎，避免资源浪费
2. **按需会话**：每个请求获得独立的数据库会话，确保事务隔离
3. **优雅启停**：应用启动时初始化连接，关闭时优雅释放资源
4. **依赖注入**：通过 FastAPI 的依赖注入系统轻松获取数据库会话
5. **连接池管理**：可配置的连接池参数，优化性能
6. **异常处理**：自动回滚失败的事务，确保数据一致性
7. **环境隔离**：支持不同环境使用不同的数据库配置

## 用 SQLAlchemy ORM 定义你的第一张数据表

基于 SQLAlchemy 2.0 现代化语法，从零开始定义健壮的数据模型，学习 Pydantic 模型与 ORM 的无缝协作，掌握 Mixin 模式编写可复用时间字段的高级技巧。


### 规范化项目结构

在上一章，为了快速演示，我们把 ORM 的基类 Base 放在了数据库连接文件里。这对于小型项目来说没问题，但随着项目变大，更好的做法是将所有与数据模型相关的代码集中管理。

#### 创建 models 目录结构

```bash
mkdir -p app/models
mkdir -p app/schemas
touch app/models/__init__.py
touch app/schemas/__init__.py
```

我们将在 app/ 目录下创建如下结构：

```
app/
├── models/          # 数据库模型（ORM）
│   ├── __init__.py  # 让 models 成为一个 Python 包
│   ├── base.py      # 存放我们的 ORM 基类
│   ├── mixin.py     # 可复用的 Mixin 类
│   └── user.py      # 存放 User 模型
└── schemas/         # API 模型（Pydantic）
    ├── __init__.py
    └── user.py      # 用户相关的 Pydantic 模式
```

#### 创建 ORM 基类

在 `app/models/base.py` 中定义所有 ORM 模型的基础类：

```python
# app/models/base.py
from sqlalchemy.orm import DeclarativeBase

# 定义所有 ORM 模型的基础类
class Base(DeclarativeBase):
    pass
```

将 Base 单独放在这里，意味着所有的数据模型都有一个统一的、可追溯的源头。

### 定义 User 模型

现在，我们来定义绝大多数应用的核心——用户模型。在 `app/models/user.py` 中：

```python
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
```

**代码解析：**

- `__tablename__`: 明确告诉 SQLAlchemy，这个类对应数据库中的 users 表
- `Mapped[type]`: 这是 SQLAlchemy 2.0 的标志性语法。它结合了 Python 的类型提示，让编辑器和静态分析工具能更好地理解你的代码
- `mapped_column()`: 这是定义列属性的核心函数
- `primary_key=True`: 将 id 设为主键
- `autoincrement=True`: id 会自动增长
- `String(64)`: 定义了一个最大长度为 64 的字符串，对应 SQL 中的 VARCHAR(64)
- `index=True`: 为 username 创建索引，加快查询速度
- `unique=True`: 保证所有用户的 username 都是唯一的
- `nullable=False`: username 字段不允许为空

### 创建 Pydantic 模式

数据库模型（ORM）和 API 模型（Pydantic）应分离。我们的 User 模型是为数据库存储而设计的，它包含了像 password_hash 这样的敏感信息。在 API 交互中，我们绝不希望将密码哈希直接返回给前端。

在 `app/schemas/user.py` 中创建 API 专用的数据模型：

```python
# app/schemas/user.py
from pydantic import BaseModel

# 基础模型，包含所有用户共有的字段
class UserBase(BaseModel):
    username: str

# 创建用户时，从请求体中读取的模型
# 需要提供密码
class UserCreate(UserBase):
    password: str

# 从数据库读取并返回给客户端的模型
# 不应该包含密码，但应该包含 id
class UserResponse(UserBase):
    id: int
    # Pydantic V2 的新配置方式
    class Config:
        from_attributes = True  # 告诉 Pydantic 模型可以从 ORM 对象属性中读取数据

```

**模式说明：**

- `UserBase`: 包含用户的基础字段，其他模式可以继承它
- `UserCreate`: 用于创建用户的请求体，包含密码字段
- `UserResponse`: 用于返回给客户端的响应，不包含敏感信息

### 使用 Mixin 模式实现可复用时间字段

在实际项目中，几乎每个表都需要 `created_at` 和 `updated_at` 字段。我们希望这些时间戳绝对精确，且不受应用服务器时钟偏差的影响。最佳实践是：将时间管理完全交给数据库服务器。
这时，“混入”（Mixin）模式就登场了。我们创建一个专门的 DateTimeMixin 类来封装这个逻辑，避免重复代码。

在 `app/models/mixin.py` 中创建时间字段 Mixin：

```python
# app/models/mixin.py
from datetime import datetime  

from sqlalchemy import func
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP  

class DateTimeMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),     # 用 PostgreSQL 方言，等价于 DateTime(timezone=True)
        # DateTime(timezone=True),    # 更通用的写法，你可以直接使用这个，去掉上面的 TIMESTAMP
        server_default=func.now(),    # 插入时由 PG 生成，采用服务器时间        
        insert_sentinel=False,        # 禁止 ORM 隐式写入
        nullable=False,               # 不允许为空  
        index=True,                   # 可通过创建时间索引
    )  

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),     # 用 PostgreSQL 方言，等价于 DateTime(timezone=True) 
        # DateTime(timezone=True),    # 更通用的写法，你可以直接使用这个，去掉上面的 TIMESTAMP
        server_default=func.now(),    # 插入时由 PG 生成，采用服务器时间
        onupdate=func.now(),          # 更新时由 PG 刷新，采用服务器时间        
        insert_sentinel=False,        # 禁止 ORM 隐式写入
        nullable=False,
    )
```

**Mixin 特性说明：**

- `server_default=func.now()`: 创建一条新记录时，该字段的默认值由数据库服务器(数据库服务器单一，保证所有时间戳的绝对权威和统一)的 NOW() 函数生成，确保时间的准确性
- `onupdate=func.now()`: 每次更新记录时由数据库服务器自动刷新 updated_at 字段
- `insert_sentinel=False`: 禁止 ORM 在插入时隐式写入时间值
- `TIMESTAMP(timezone=True)`:  PostgreSQL 方言中的类型，使用带时区的时间戳，避免时区问题

### 更新数据库连接模块

为了解决数据表创建问题，我们需要确保所有模型都被正确导入和注册。

#### 更新 models 包的 __init__.py

在 `app/models/__init__.py` 中导入所有模型：

```python
# app/models/__init__.py

# 导入 Base，它是所有模型的基础
from .base import Base
# 导入你所有的模型，确保它们被 Base.metadata 识别
from .user import User
# 如果未来有其他模型，比如 Post, Item，也在这里导入
# from .post import Post
# from .item import Item

# 可选：使用 __all__ 来明确声明这个包对外暴露的接口
# 这是一种良好的编程习惯
__all__ = ["Base", "User"]
```

#### 修复数据库会话模块

更新 `app/db/session.py`，使用统一的 Base 类：

```python
# 在文件顶部，移除原来的 Base 定义，改为导入
from app.models.base import Base
```

#### 更新主应用文件

在 `app/main.py` 中导入模型包，确保所有模型被注册：

```python
# 在导入部分添加
# 导入所有模型，确保它们被注册到 Base.metadata 中
import app.models
```

### 数据库表创建和测试

#### 启动 PostgreSQL 数据库

使用 Docker 启动 PostgreSQL 容器：

```bash
docker run --name postgres-demo \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=tutorial \
  -p 5432:5432 \
  -d postgres:15
```

#### 运行应用并创建表

启动开发服务器：

```bash
uv run --env-file env.dev -- fastapi dev
```

应用启动时会自动创建数据库表（在开发环境中）。
打开数据库连接工具查看生成的数据表

### 核心特性总结

我们构建的 ORM 数据层具有以下特性：

1. **现代化语法**: 使用 SQLAlchemy 2.0 的 `Mapped` 和 `mapped_column` 语法
2. **类型安全**: 完整的类型注解支持，提供更好的 IDE 体验
3. **模块化设计**: 清晰的目录结构，分离关注点
4. **可复用组件**: Mixin 模式实现通用字段的复用
5. **API 安全**: Pydantic 模式确保敏感数据不会意外暴露
6. **自动化时间管理**: 数据库服务器自动管理时间字段
7. **开发友好**: 自动表创建和测试端点，便于开发调试

## 优雅地处理错误，构建强大的自定义异常系统

在真实的应用中，错误处理是不可避免的核心主题。用户可能查询不存在的资源、尝试注册已占用的用户名，或者数据库连接突然失败。我们需要构建一套健壮而优雅的异常处理机制，作为应用的"免疫系统"。

### 为什么要自定义异常？

FastAPI 自带的 `HTTPException` 虽然方便，但在大型项目中会遇到以下问题：

1. **代码重复**：在各个角落重复写 `status_code=404`、`status_code=409`
2. **职责不清**：业务逻辑与表现层逻辑混合(业务逻辑（例如，“找不到某个项目”）和表现层逻辑（“应该返回 404 状态码”）混在了一起)，深层业务代码不应关心 HTTP 状态码
3. **语义模糊**：`HTTPException(status_code=404)` 远不如 `ItemNotFoundException` 清晰易读

### 设计业务异常体系

我们的目标是在代码中写 `raise UserNotFoundException()`，然后让 FastAPI 自动转换成标准的 HTTP 404 响应。


#### 创建异常处理模块

在 `app/core/exceptions.py` 中创建自定义异常系统：

```python
# app/core/exceptions.py
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from loguru import logger

# ------------------ 业务异常: 继承自 HTTPException，所以 FastAPI 能直接处理 ------------------

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class AlreadyExistsException(HTTPException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Unauthorized access"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

# ------------------ 全局兜底: 捕获所有未被处理的异常 ------------------

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # 使用 loguru 记录详细的异常信息，包括堆栈跟踪
    logger.exception(f"Unhandled exception at {request.url.path}: {exc}")
    # 向客户端返回一个通用的、安全的错误信息
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
```

**代码解析：**
- **业务异常**：继承自 FastAPI 的 `HTTPException`，FastAPI 内置错误处理中间件能识别它们
- **预设状态码**：在 `__init__` 方法中预设状态码和默认提示信息，也可以自定义提示信息：raise NotFoundException(detail="Hero with id 123 not found")
- **全局兜底**：`global_exception_handler` 捕获所有未处理的异常，记录详细日志并返回安全的错误信息

#### 注册全局异常处理器

在 `app/main.py` 中注册异常处理器：

```python
# 导入全局异常处理函数
from app.core.exceptions import global_exception_handler

app = FastAPI(
    title=settings.APP_NAME,
    description="这是一个 FastAPI 演示项目",
    version=get_project_version(),
    lifespan=lifespan
)

# 将 global_exception_handler 注册为处理所有 Exception 类型（及其子类）的处理器
# 这会捕获所有类型为 Exception 的异常
app.add_exception_handler(Exception, global_exception_handler)
```

#### 添加异常测试端点

为了验证异常处理系统，我们添加一些测试端点：

```python
# --- 异常处理测试端点 ---
from app.core.exceptions import (
    NotFoundException,
    AlreadyExistsException,
    UnauthorizedException,
    ForbiddenException,
)

@app.get("/test-exceptions/not-found")
async def test_not_found():
    """
    测试 404 异常处理
    """
    raise NotFoundException("测试资源未找到")

@app.get("/test-exceptions/already-exists")
async def test_already_exists():
    """
    测试 409 冲突异常处理
    """
    raise AlreadyExistsException("测试资源已存在")

@app.get("/test-exceptions/unauthorized")
async def test_unauthorized():
    """
    测试 401 未授权异常处理
    """
    raise UnauthorizedException("测试未授权访问")

@app.get("/test-exceptions/forbidden")
async def test_forbidden():
    """
    测试 403 禁止访问异常处理
    """
    raise ForbiddenException("测试禁止访问")

@app.get("/test-exceptions/server-error")
async def test_server_error():
    """
    测试 500 服务器错误异常处理（全局异常处理器）
    ValueError 是 Python 的标准异常， 不是 HTTPException 的子类，FastAPI 无法直接处理非 HTTPException 类型的异常
    FastAPI 会将其传递给全局异常处理器
    """
    # 故意抛出一个未被捕获的异常，触发全局异常处理器
    raise ValueError("这是一个测试用的服务器内部错误")
```

### 测试异常处理系统

#### 启动应用

```bash
uv run --env-file env.dev -- fastapi dev
```

#### 测试各种异常

访问以下端点测试异常处理：

1. **404 异常**：`http://127.0.0.1:8000/test-exceptions/not-found`
   - 返回：`{"detail": "测试资源未找到"}`，状态码 404

2. **409 冲突异常**：`http://127.0.0.1:8000/test-exceptions/already-exists`
   - 返回：`{"detail": "测试资源已存在"}`，状态码 409

3. **401 未授权异常**：`http://127.0.0.1:8000/test-exceptions/unauthorized`
   - 返回：`{"detail": "测试未授权访问"}`，状态码 401

4. **403 禁止访问异常**：`http://127.0.0.1:8000/test-exceptions/forbidden`
   - 返回：`{"detail": "测试禁止访问"}`，状态码 403

5. **500 服务器错误**：`http://127.0.0.1:8000/test-exceptions/server-error`
   - 返回：`{"detail": "Internal server error"}`，状态码 500
   - 控制台会记录详细的异常堆栈信息

### 异常处理系统的优势

1. **语义化**：异常名称直接表达业务含义，代码更易读
2. **可复用**：一次定义，全项目使用，避免重复代码
3. **集中管理**：所有异常定义集中在一个文件中，便于维护
4. **职责分离**：业务层只关心"发生了什么"，不关心"返回什么状态码"
5. **安全性**：全局异常处理器确保敏感信息不会泄露给客户端
6. **可观测性**：详细的日志记录帮助快速定位和解决问题

### 在实际业务中的应用

在后续的用户管理、数据库操作等功能中，我们可以这样使用：

```python
# 在用户服务中
if not user:
    raise NotFoundException(f"用户 {user_id} 不存在")

if existing_user:
    raise AlreadyExistsException(f"用户名 {username} 已被占用")

# 在权限检查中
if not has_permission:
    raise ForbiddenException("您没有权限执行此操作")
```

这样的代码既清晰又专业，为后续的仓库层和路由层开发奠定了坚实的基础。

## 深入仓库层(Repository)，实现优雅的数据库操作

基于仓库模式(Repository Pattern)构建专业、可维护的数据访问层，将所有数据库操作逻辑封装起来，并与自定义异常完美结合。

### 什么是仓库模式 (Repository Pattern)？

仓库模式是一个专门负责与数据库打交道的"数据专家"，把所有数据访问逻辑（增、删、改、查）都封装在自己内部，让其他代码（比如服务层）无需关心数据库的具体实现。

#### 核心优势

- **🎯 职责分离 (Separation of Concerns)**: 让业务逻辑回归业务，数据访问回归数据。服务层只需要说"给我一个具体的数据"，而不用关心你是从 MySQL 还是 PostgreSQL 中 SELECT 出来的。
- **🔧 易于测试 (Testability)**: 当测试服务层时，我们可以轻松地用一个"假的"内存仓库来代替真实的数据库连接，让单元测试变得飞快且独立。
- **🔄 代码复用 (Reusability)**: get_by_id 这种通用操作只需编写一次，就可以被任何需要它的地方安全调用，一劳永逸。

### 准备工作：创建英雄(Hero)模型

为了完整地演示增删改查（CRUD），我们创建一个简单的示例：一个 Hero (英雄) 模型。

#### 创建 ORM 模型

```python
# app/models/heroes.py
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Hero(Base):
    __tablename__ = "heroes"
    # 一个英雄的表，包含了名字以及称号两个字段
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    alias: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<Hero(id={self.id!r}, name={self.name!r}, alias={self.alias!r})>"
```

#### 创建 Pydantic 模型

```python
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
```

### 构建 HeroRepository

#### 创建仓库目录结构

为了更好地体现"按领域驱动"的设计思想，我们将与 Hero 相关的所有业务逻辑代码（仓库层、服务层）都统一收纳到 `app/domains/heroes/` 目录下。

```bash
mkdir -p app/domains/heroes
touch app/domains/heroes/__init__.py
```

#### 实现 HeroRepository

```python
# app/domains/heroes/heroes_repository.py
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def get_all(self) -> list[Hero]:
        """Fetch all heroes."""
        query = select(Hero)
        result = await self.session.scalars(query)
        return list(result.all())

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
```

#### HeroRepository 实现说明

**1. 构造函数 `__init__`：依赖注入，一切的起点**

```python
def __init__(self, session: AsyncSession):
    self.session = session
```

- **实现思路：** 这是我们整个仓库类与外界（主要是数据库）沟通的唯一桥梁。我们没有在仓库内部通过 `create_engine` 或 `sessionmaker` 来创建数据库会话 (`session`)，而是**通过构造函数参数的形式把它“要”进来**。

- **为什么这么做？** 这就是大名鼎鼎的**依赖注入（Dependency Injection）**思想。把它想象成一个星级大厨（`HeroRepository`）：他不需要自己去建一个烤箱（`session`），而是厨房（FastAPI的依赖系统）直接为他提供一个预热好的顶级烤箱。这样做的好处是：

- - **解耦：** 仓库不用关心数据库连接是怎么建立的、地址是什么。它只管用。
  - **易测试：** 在单元测试中，我们可以轻松地传入一个“假的”内存数据库会话来测试仓库的逻辑，而无需启动真实的数据库。

**2. `create` 方法：不只是新增，更是安全的守护者**

```python
async def create(self, hero_data: HeroCreate) -> Hero:
    hero = Hero(**hero_data.model_dump())
    try:
        self.session.add(hero)
        await self.session.commit()
        await self.session.refresh(hero)
        return hero
    except IntegrityError:
        await self.session.rollback()
        raise AlreadyExistsException(...)
```

**实现思路：** 这个方法负责将一个 Pydantic 数据模型 (`HeroCreate`) 转换为 ORM 模型 (`Hero`)，并将其持久化到数据库中。

- `hero = Hero(**hero_data.model_dump())`：这是 Pydantic V2 的标准用法，`model_dump()` 将输入数据转换成一个字典，`**` 操作符则像魔法一样将字典解包，作为参数传递给 `Hero` 类的构造函数来创建实例。
- `session.add(hero)`：将新创建的 `hero` 对象放入 SQLAlchemy 的“暂存区”。
- `await self.session.commit()`：将“暂存区”的所有更改一次性提交到数据库，这是一个原子操作。
- `await self.session.refresh(hero)`：**这是非常关键的一步！** 提交后，我们的 `hero` Python 对象其实并不知道数据库为它生成的 `id` 是多少。`refresh` 操作会用数据库中的最新数据（包括自增的 `id`）来更新这个 Python 对象。
- `except IntegrityError...`：**这是我们与上一篇文章的第一次完美联动！** 当 `alias` 字段因为 `unique=True` 约束而插入重复值时，数据库会抛出 `IntegrityError`。我们在这里捕获这个底层的、不友好的错误，然后 `rollback()` 撤销失败的事务，最后抛出我们自己定义的、富有业务含义的 `AlreadyExistsException`。

 **3. `get_by_id` 方法：没有就是没有，绝不含糊**

```python
async def get_by_id(self, hero_id: int) -> Hero:
    hero = await self.session.get(Hero, hero_id)
    if not hero:
        raise NotFoundException(...)
    return hero
```

- **实现思路：** 这是最基础的查询操作。我们使用 SQLAlchemy 2.0 推荐的 `session.get()` 方法，它专门用于通过主键进行高效查询。
- **为什么不返回 `None`？** 很多初学者可能会想，如果找不到，直接 `return None` 不就好了吗？但这是一个潜在的“坑”。如果返回 `None`，那么调用这个函数的上层代码就必须每次都写 `if hero is not None:` 来做判断，一旦忘记，就会在访问 `hero.name` 时出现 `AttributeError: 'NoneType' object has no attribute 'name'` 的致命错误。
- **第二次完美联动：** 我们的做法是，**将“不存在”这种情况视作一种业务异常**。如果 `hero` 是 `None`，我们立即抛出 `NotFoundException`。这强制了上层代码必须处理这个异常，或者让 FastAPI 的全局异常处理器来捕获它并返回一个清晰的 `404 Not Found` 响应。代码更健壮，意图也更清晰。

**4. `get_all` 方法：简单，但为未来而生**

```python
async def get_all(self) -> list[Hero]:
    query = select(Hero)
    result = await self.session.scalars(query)
    return list(result.all())
```

- **实现思路：** 这个方法目前非常简单，使用 `select(Hero)` 创建一个查询所有英雄的语句，然后通过 `session.scalars()` 执行它。`scalars()` 是一个方便的方法，当我们确定查询只返回单个实体（比如 `Hero` 对象本身，而不是它的多个字段元组）时，它能让我们直接获取这些对象。

- **为未来做铺垫：** 你可能会想，如果英雄有几千个，一次性全部查出来岂不是要撑爆内存？你说得对！目前这个实现是最基础的版本。在后续的教程中，我们会对它进行**终极进化**：

- - **增加分页：** 添加 `skip` 和 `limit` 参数。
  - **增加排序：** 添加 `order_by` 参数来决定按 `id` 还是 `name` 排序。
  - **增加过滤：** 添加 `name_filter` 等参数，实现按条件搜索。
    这个简单的方法，是我们未来构建复杂查询功能的一个完美起点。

**5. `update` 方法：复用与细节的艺术**

```python
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
```

- **实现思路：** 更新操作的第一步，永远是“先找到要更新的目标”。
- `hero = await self.get_by_id(hero_id)`：我们在这里没有重写一遍查询逻辑，而是**机智地复用了 `get_by_id` 方法**。这不仅代码更简洁，还自动“继承”了 `get_by_id` 在找不到英雄时抛出 `NotFoundException` 的优秀特性。
- `hero_data.model_dump(exclude_unset=True)`：**这是实现 HTTP PATCH（部分更新）的精髓！** `exclude_unset=True` 告诉 Pydantic：“只把用户在请求中明确传递的字段导出为字典，那些没传的（即保持默认值的）字段就忽略它们”。这样，即使用户只传了一个 `name`，`alias` 字段也不会被意外地更新成 `None`。
- `for key, value in ... setattr(hero, key, value)`：这是一个动态更新对象的优雅方式。无论将来 `HeroUpdate` 模型增加多少字段，这段代码都无需修改，因为它会自动遍历所有传入的字段并进行赋值。

 **6. `delete` 方法：沉默是金，成功无需多言**

```python
async def delete(self, hero_id: int) -> None:
    hero = await self.get_by_id(hero_id)
    await self.session.delete(hero)
    await self.session.commit()
```

- **实现思路：** 和更新一样，删除也先通过复用`get_by_id`来找到目标并处理好“未找到”的异常情况。核心操作就是 `session.delete(hero)`。
- **为什么返回值是 `None`？** 这是遵循一个重要的设计原则：**命令-查询分离 (CQS)**。删除是一个“命令”操作，它的成功状态就是“没有抛出异常”。它不需要返回任何数据。
- **为API层设计：** 这个 `-> None` 的返回类型注解，是给未来API层的一个明确信号。在后续构建路由端点的文章中，我们会看到，处理这个请求的API函数可以利用这一点，在成功删除后，直接向客户端返回一个 `HTTP 204 No Content` 状态码。这是一种非常规范和优雅的 RESTful API 设计实践。



### 仓库层的核心特点

1. **异常转换**: 将底层的 `IntegrityError` 转换为业务友好的 `AlreadyExistsException`
2. **事务管理**: 自动处理提交和回滚操作
3. **类型安全**: 使用 SQLAlchemy 2.0 的现代语法和类型注解
4. **错误处理**: 统一的错误处理模式，确保数据一致性



## 揭秘服务层(Service)，不止是数据库的"传声筒"

服务层是位于仓库层和路由层之间的核心组件，负责编排业务逻辑、数据转换与整合，是现代应用架构中不可或缺的"大脑"。

### 服务层的核心价值

通俗比喻：如果说仓库层是一个储备丰富的"菜市场"，它只负责提供最新鲜的原材料（数据库模型）；那么服务层就是一位技艺精湛的"厨房主厨"。

#### 核心职责

- **🧠 业务逻辑的家 (Business Logic Hub)**: 所有复杂的业务规则、流程编排、数据计算和决策，都应该在这里进行。例如，"用户积分达到1000后自动升级为VIP"这类逻辑就属于服务层。
- **🔄 数据转换与整合 (Data Transformation & Aggregation)**: 调用一个或多个仓库层方法，将获取的原始数据进行处理、计算、整合，然后转换成上层（通常是API路由）需要的格式。
- **🔗 彻底解耦 (Decoupling)**: 它是路由层与数据访问层之间的"绝缘体"。路由层只需关心"调用哪个服务"，而无需关心数据来自哪个表、经过了何种复杂的计算。

### 基础构建：精简的"瘦"服务层

#### 实现 HeroService

```python
# app/domains/heroes/heroes_services.py
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

    async def get_heroes(self,) -> list[HeroResponse]:
        heroes = await self.repository.get_all()        
        return [HeroResponse.model_validate(hero) for hero in heroes]

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
```

### 数据转换的核心价值

即便是这个"瘦"服务层，它也完成了最基础但关键的任务：数据形态转换。

关键代码：`return HeroResponse.model_validate(new_hero)`

- **作用**: 仓库层返回的 `new_hero` 是一个 SQLAlchemy 的 ORM 模型实例，它与数据库表结构紧密相关，可能包含一些不应暴露给外部的内部属性。而 `HeroResponse` 是我们定义的 Pydantic 模型，`model_validate()` 智能地从 ORM 实例中读取属性，并填充到 Pydantic 模型中，同时进行数据校验。这得益于我们在 `HeroResponse` 的 `Config` 中设置了 `from_attributes = True`。



## 依赖注入 (Depends) 的魔力，连接三层架构的魔法胶水

现在，我们的仓库层和新增的服务层都已就位，整个项目的架构已经初具雏形。我们现在面临着一个最实际的问题：在 API 路由里，我该如何得到一个配置好的服务实例，去调用它的方法呢？

答案就是依赖注入 (Dependency Injection, DI)。回到我们的项目中，通过一个具体的场景，让你亲眼见证 Depends 是如何像魔法一样，将我们分散的数据库、仓库层、服务层优雅地"粘合"在一起的。

### 困境：一个没有"魔法"的世界

如果不使用 FastAPI 的依赖注入，我们想在路由里创建一个英雄，代码会是什么样子。

我们来尝试手动实现得到一个已经配置好数据库连接的 HeroService 实例这个过程，这是一个很好的"错误"示范，它能让我们深刻体会到依赖注入所解决的痛点：

```python
# 这是一个为了说明问题的"笨办法"
@router.post("/")
async def create_hero_bad_way(hero_data: HeroCreate):
    # 步骤 1: 手动创建一个数据库会话
    async with SessionLocal() as session:
        # 步骤 2: 手动用会话来创建仓库层实例
        repository = HeroRepository(session)
        # 步骤 3: 手动用仓库层来创建服务层实例
        service = HeroService(repository)
      
        # 步骤 4: 终于可以使用服务了
        new_hero = await service.create_hero(hero_data)
        return new_hero
```

这段代码虽然能跑通，但它简直是一场灾难。想象一下，如果你的项目有几十个API端点都需要用到 HeroService，那将意味着：

• 🤢 **代码极度冗余：** 每个路由函数里都得重复上面这一大段初始化代码。这完全违背了"Don't Repeat Yourself (DRY)"的编程原则。
• 🤝 **耦合度高如磐石：** 路由层本该只关心接收请求和返回响应，现在它却被迫了解 HeroService、HeroRepository 甚至数据库 session 是如何被一层层创建的。它们被死死地绑在了一起。
• 🔧 **维护和测试的噩梦：** 某天，HeroService 的创建需要增加一个新的参数（比如一个日志记录器），你该怎么办？答案是：把每一个用到它的路由函数都找出来，逐一修改。这简直无法想象。



### 解决方案：FastAPI 的超能力 —— Depends

你可以把 Depends 理解成一个神通广大的"自动装配工"。你不再需要亲自动手组装零件，只需要在你的函数参数里，像填写订单一样声明："我需要一个功能完备的 HeroService"

然后，FastAPI 这位装配工就会自动帮你把所有需要的零件（数据库连接、仓库层实例等）全部找齐，完美组装，最后将一个立即可用的 HeroService 实例"注入"到你的函数中。

Depends 的"魔法"并非凭空产生，它背后是一套清晰、严谨的"依赖链"逻辑。现在，让我们像参观工厂的装配线一样，自底向上，一步步拆解这条链是如何在我们项目中构建的。

#### 第一站：原材料供应 —— 数据库会话 (get_db)

一切依赖的源头，是我们对数据库的连接。在讲解数据库连接的文章中，我们创建了一个至关重要的函数：

```python
# 来自 app/db/session.py
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """为每个请求提供一个独立的、自动管理的数据库会话。"""
    if _SessionFactory is None:
        raise Exception("数据库未初始化...")

    async with _SessionFactory() as session:
        yield session
```

这个函数就是我们依赖链的第一环，一个"可依赖项 (Dependable)"。让我们深入理解 yield 在这里的精妙之处：

1. `async with _SessionFactory() as session:`
   当一个请求需要数据库时，这行代码会从我们全局的连接池里取出一个连接，并开启一个会话 session。

2. `yield session:`
   这是最关键的一步！它就像一个暂停按钮。代码执行到这里，会把 session 对象交出去，让需要它的函数（比如我们的路由函数）先使用。函数自身则在这里暂停等待。

3. (请求处理中...)
   路由函数拿着 session 去执行各种数据库操作。

4. (请求处理结束)
   当路由函数执行完毕并返回后，FastAPI 会回到 yield 的地方，继续往下执行。async with 语句的特性保证了无论成功还是异常，会话都会被自动关闭，连接被安全地还回连接池。

get_db 完美地解决了"按需提供，用完即收"的资源管理问题。

#### 第二站：零件加工 —— 仓库层 (HeroRepository)

有了原材料 session，我们并不会直接把它交给最终的"主厨"（服务层）。我们会先把它交给专门负责数据操作的"专家"（仓库层）。

回顾一下我们的 HeroRepository 定义：

```python
# 来自 app/domains/heroes/heroes_repository.py
class HeroRepository:
    """仓库层，负责处理英雄相关的数据库操作。"""
    def __init__(self, session: AsyncSession):
        self.session = session

    # ... (create, get_by_id, update 等方法)
```

看它的 `__init__` 方法，它明确声明："我需要一个 AsyncSession 才能工作！" 仓库层是与数据库打交道的专家，它需要一个数据库会话才能执行所有增删改查的操作。

#### 第三站：成品组装 —— 服务层 (get_hero_service)

现在，我们来到了最关键的总装车间。我们的目标是得到一个 HeroService 实例。服务层本身的设计是怎样的呢？

```python
# 来自 app/domains/heroes/heroes_services.py
class HeroService:
    def __init__(self, repository: HeroRepository):
        self.repository = repository
    # ... (create_hero, get_hero_with_story 等方法)
```

HeroService 的 `__init__` 也提出了它的要求："我不需要数据库连接，我只需要一个已经能工作的 HeroRepository！"

这就是解耦！服务层只负责指挥，不关心具体执行的细节。

那么，谁来完成这个"用 session 创建 repository，再用 repository 创建 service"的组装任务呢？答案就是我们的依赖函数 get_hero_service：

```python
# 我们通常会把它放在 service 文件或一个专门的 dependencies.py 文件里
def get_hero_service(session: AsyncSession = Depends(get_db)) -> HeroService:
    """这是一个依赖函数，负责组装并返回 HeroService 的实例。"""
    # 步骤 1: 用依赖注入的 session 创建 repository
    repository = HeroRepository(session)
    # 步骤 2: 用创建好的 repository 创建 service
    return HeroService(repository)
```

这段代码完美地展示了依赖的"套娃"模式。让我们来揭示 FastAPI 在背后上演的"偷天换日"：

1. 当一个路由声明它需要 `Depends(get_hero_service)` 时，FastAPI 开始执行 get_hero_service 函数。
2. 它立刻发现 get_hero_service 的参数 session 依赖于 `Depends(get_db)`。
3. 于是，FastAPI 暂停 get_hero_service 的执行，转头先去运行 get_db，从第一站拿到了原材料 session。
4. FastAPI 将这个 session 对象，作为参数传递给 get_hero_service。
5. get_hero_service 内部的代码开始执行：
   • `repository = HeroRepository(session)`：第二站启动！用 session 加工出了一个 repository 零件。
   • `return HeroService(repository)`：第三站完成！用 repository 零件组装出了 service 成品。
6. 最后，这个新鲜出炉、功能完备的 service 实例被 return，并最终注入到我们的路由函数中。

现在，这条完整的装配线变得无比清晰：
**路由函数 → get_hero_service (组装 service 和 repository) → get_db (提供 session)**



### 最终装配：在路由中享受优雅

现在，我们终于可以写出那个最终的、极度优雅的路由函数了。

```python
# 在你的路由文件中
from app.domains.heroes.heroes_dependencies import get_hero_service

@router.post("/", response_model=HeroResponse)
async def create_hero(
    hero_data: HeroCreate,
    service: HeroService = Depends(get_hero_service)  # 看这里！
):
    return await service.create_hero(hero_data)
```

让我们再次把它和第一节中的"笨办法"对比一下：

• **干净、简洁：** 路由函数恢复了它本来的面目，只关心接收数据和调用服务这两个核心职责。
• **完全解耦：** 路由对 HeroService 的内部构造一无所知。它只知道"我需要一个服务"，至于这个服务是哪里来的、怎么来的，一概不关心。
• **极致复用：** 我们可以像贴贴纸一样，在任何需要 HeroService 的地方，轻松地贴上 `Depends(get_hero_service)`。



### 依赖注入的核心价值

通过今天的实战，我们知道了依赖注入远不止是一个"语法糖"，它是一种能从根本上提升项目质量的架构思想。

• ✅ **可维护性 (Maintainability)**: 如果未来 HeroService 需要一个新的依赖，比如缓存服务 RedisCache。我们只需要修改 get_hero_service 这一个地方，所有依赖它的路由都会自动获得这个新能力，无需任何改动！
• ✅ **可测试性 (Testability)**: 这是 DI 带来的巨大福音。在写单元测试时，我们可以轻松地告诉 FastAPI："嘿，测试的时候，当遇到 `Depends(get_hero_service)`，请不要用真的，用我给你的这个 FakeHeroService 来代替！"（这个高级技巧我们会在后续测试章节深入讲解）。
• ✅ **代码清晰 (Clarity)**: 一个函数的签名 (def ...(...)) 就是一份清晰的"依赖清单"，直接告诉了我们它正常工作所需要的一切。



## 构建完整的 API 路由层

基于三层架构的设计原则，构建专业的 API 路由层，实现 HTTP 请求处理、依赖注入和统一的响应格式。

### 创建英雄 API 路由

#### 创建路由目录

```bash
mkdir -p app/api/v1
touch app/api/v1/__init__.py
```

#### 实现英雄路由

```python
# app/api/v1/heroes_route.py
from loguru import logger
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.domains.heroes.heroes_repository import HeroRepository
from app.domains.heroes.heroes_services import HeroService
from app.schemas.heroes import HeroCreate, HeroUpdate, HeroResponse, HeroStoryResponse


router = APIRouter(prefix="/heroes", tags=["Heroes"])


# 依赖注入
def get_hero_service(session: AsyncSession = Depends(get_db)) -> HeroService:
    """Dependency for getting HeroService instance."""
    repository = HeroRepository(session)
    return HeroService(repository)


@router.post("", response_model=HeroResponse, status_code=status.HTTP_201_CREATED)
async def create_hero(
    data: HeroCreate, service: HeroService = Depends(get_hero_service)
) -> HeroResponse:
    """Create new hero."""
    try:
        created_hero = await service.create_hero(data=data)
        logger.info(f"Created hero with id: {created_hero.id}")
        return created_hero
    except Exception as e:
        logger.error(f"Failed to create hero: {e}")
        raise


@router.get("", response_model=list[HeroResponse])
async def get_all_heroes(
    service: HeroService = Depends(get_hero_service),
) -> list[HeroResponse]:
    """Get all heroes."""
    try:
        all_heroes = await service.get_heroes()
        logger.info(f"Retrieved {len(all_heroes)} heroes")
        return all_heroes
    except Exception as e:
        logger.error(f"Failed to fetch all heroes: {e}")
        raise


@router.get("/{hero_id}", response_model=HeroResponse)
async def get_hero(
    hero_id: int,
    service: HeroService = Depends(get_hero_service),
) -> HeroResponse:
    """Get hero by id."""
    try:
        hero = await service.get_hero(hero_id=hero_id)
        logger.info(f"Retrieved hero {hero_id}")
        return hero
    except Exception as e:
        logger.error(f"Failed to get hero {hero_id}: {e}")
        raise


@router.patch("/{hero_id}", response_model=HeroResponse, status_code=status.HTTP_200_OK)
async def update_hero(
    data: HeroUpdate,
    hero_id: int,
    service: HeroService = Depends(get_hero_service),
) -> HeroResponse:
    """Update hero."""
    try:
        updated_hero = await service.update_hero(data=data, hero_id=hero_id)
        logger.info(f"Updated hero {hero_id}")
        return updated_hero
    except Exception as e:
        logger.error(f"Failed to update hero {hero_id}: {e}")
        raise


@router.delete("/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hero(
    hero_id: int,
    service: HeroService = Depends(get_hero_service),
) -> None:
    """Delete hero."""
    try:
        await service.delete_hero(hero_id=hero_id)
        logger.info(f"Deleted hero {hero_id}")
    except Exception as e:
        logger.error(f"Failed to delete hero {hero_id}: {e}")
        raise
  
  
@router.get("/{hero_id}/story", response_model=HeroStoryResponse)
async def generate_hero_story(
    hero_id: int,
    service: HeroService = Depends(get_hero_service),
) -> HeroResponse:
    """Generate hero story."""
    try:
        story = await service.get_hero_with_story(hero_id=hero_id)
        logger.info(f"Generated story for hero {hero_id}")
        return story
    except Exception as e:
        logger.error(f"Failed to generate hero's story for hero_id={hero_id}: {e}")
        raise
```

#### 设计决策的精髓

**一、 让路由层“变笨”——优雅的异常处理模式**

你可能注意到了，我们每个路由端点中都有一个看起来一模一样的 `try...except...raise` 结构：

```
try:
    # ... call service layer ...
except Exception as e:
    logger.error(f"Failed to ...: {e}")
    raise # 关键在这里！
```

这和许多初学者（甚至是一些项目）直接在路由里写 `raise HTTPException(status_code=404, ...)` 的做法截然不同。我们为什么要这么做？

这背后是一种极其重要的架构思想：**职责分离 (Separation of Concerns)**。

我们的路由层被设计成一个“**无知的传达者**”。它只关心三件事：

1. 接收 HTTP 请求。
2. 调用相应的服务层方法来处理业务逻辑。
3. 如果发生任何异常，**用日志记录下这个异常发生的上下文**（例如，“在创建英雄时失败了”），然后**原封不动地将异常再次抛出**。

路由层**完全不关心** `NotFoundException` 应该对应 HTTP `404` 还是 `409`。它变“笨”了，但也因此变得更加纯粹和稳定。

真正的“翻译”工作，交给了我们之前构建的**全局异常处理系统**。这就像一条从仓库层到最终 HTTP 响应的“**异常直通车**”：

- **仓库层**：识别出“数据未找到”，抛出 `NotFoundException`。
- **服务层**：作为透明管道，直接传递异常。
- **路由层**：捕获异常，记录日志，然后再次抛出。
- **FastAPI 全局处理器**：接收到 `NotFoundException`，因为我们让它继承自 `HTTPException`，FastAPI 就知道要将其“翻译”成一个 `404` 的 JSON 响应返回给客户端。

**这种模式的好处是巨大的：** 业务逻辑（发生了什么错误）和表现逻辑（该如何响应这个错误）彻底解耦。未来无论我们想修改错误信息，还是调整状态码，都只需要在 `exceptions.py` 中修改一处即可，而无需触碰任何路由代码。

**二、 API 的“协议语言”——精通 HTTP 状态码**

一个专业的 API，会像一个健谈而严谨的人一样，使用精确的语言与客户端沟通。HTTP 状态码就是这门语言。

- `status_code=status.HTTP_201_CREATED`：在 `POST` 请求中使用，明确告诉客户端：“你请求的资源**已成功创建**。” 这比含糊的 `200 OK` 语义更精确，是 RESTful 风格的标志。
- `status_code=status.HTTP_204_NO_CONTENT`：在 `DELETE` 请求中使用，这是 RESTful API 的最佳实践。它传达了两个信息：“1. 你的删除请求已成功执行。2. 我不会在响应体中返回任何内容。” FastAPI 足够智能，会确保在这种情况下响应体为空。
- `status_code=status.HTTP_200_OK`：在 `GET` 和 `PATCH` 中使用，表示操作成功，并且我在响应体中返回了你请求或更新后的资源。

正确使用状态码，不仅仅是“为了好看”，它是一种**API 设计契约**。它让前端、移动端或其他微服务的开发者能轻松、可预测地与我们的 API 交互，也让监控和调试变得更加简单。

**三、 依赖的“领域内聚”——思考 get_hero_service 的位置**

你可能也注意到了，`get_hero_service` 这个依赖提供函数，我们是直接写在了 `heroes_route.py` 文件的顶部，而不是放在一个全局的 `dependencies.py` 文件里。

```
# 在路由文件顶部定义
def get_hero_service(session: AsyncSession = Depends(get_db)) -> HeroService:
    repository = HeroRepository(session)
    return HeroService(repository)
```

这是一个经过深思熟虑的**设计决策**，它体现了 **高内聚（High Cohesion）** 的原则。

- **优点（高内聚）**：

- - **清晰自洽**：任何阅读此文件的人，都能立刻明白这个“英雄”模块所依赖的服务是如何构建的，所有相关逻辑都集中在一个地方。
  - **模块独立**：`heroes` 模块是自包含的。未来想把这个功能模块整体迁移到另一个项目，或者进行重构时，会非常方便，因为它的核心依赖关系都在内部定义好了。

当然，这种做法也有潜在的权衡。如果未来另一个模块（比如 `teams_route.py`）也需要 `HeroService`，就可能需要复制代码或重新导入。但对于像 `HeroService` 这样 **领域高度特定（Domain-Specific）** 的服务，将其依赖与使用它的路由放在一起，通常是利大于弊的。它让我们的代码库在逻辑上划分得像一个个“乐高积木”，而不是一团乱麻。



### 注册路由到主应用

更新 `app/main.py` 以包含新的路由：

```python
# /fastapi-demo-project/app/main.py
...
from app.api.v1 import heroes_route # 导入我们创建的路由模块

app = FastAPI(
    title=settings.APP_NAME,
    description="这是一个 FastAPI 演示项目",
    # 动态从 pyproject.toml 读取版本号
    version=get_project_version(),
    lifespan=lifespan
)

# 将英雄路由注册到主应用中
app.include_router(heroes_route.router, prefix="/api/v1")

```

### 路由层的核心特点

1. **依赖注入**: 通过 `Depends` 自动注入服务层实例
2. **异常处理**: 将业务异常转换为适当的 HTTP 状态码
3. **类型安全**: 使用 Pydantic 模型确保请求和响应的类型安全
4. **RESTful 设计**: 遵循 REST API 设计原则
5. **文档自动生成**: FastAPI 自动生成 OpenAPI 文档

## 用 Alembic 配置数据库迁移入门指南

在上一章中，我们成功构建了完整的 API 路由层，实现了从 HTTP 请求到底层数据库操作、再到优雅 JSON 响应的完整工作闭环。我们的项目，从一个想法，真正变成了可交互、可使用的服务。但随着项目"活"起来，一个更严肃、更具挑战性的问题也浮出水面：我们该如何管理我们数据库的"生命"？

### 从临时方案到专业级数据库管理

在项目初期，我们使用 `create_db_and_tables()` 函数来创建数据库表，这种方式简单直接，但随着项目发展，它的局限性逐渐暴露：

**现有方案的问题**：
- **单向操作**：只能创建表，无法处理结构变更
- **缺乏版本控制**：无法追踪数据库结构的演进历史
- **环境不一致**：开发、测试、生产环境可能出现结构差异
- **安全风险**：应用程序拥有过高的数据库权限

**真实场景挑战**：
假设我们的 `Hero` 模型需要添加 `powers` 字段来描述英雄能力。在生产环境中，数据库已存储大量数据，我们需要：
- 安全地修改表结构
- 保证数据完整性
- 确保所有环境同步更新
- 提供回滚机制

这时，我们需要引入专业的数据库迁移工具 —— **Alembic**。

### Alembic 核心概念与架构

**什么是 Alembic？**
Alembic 是 SQLAlchemy 作者开发的轻量级数据库迁移工具，专门用于管理数据库结构的版本化变更。

**核心特性**：
- **版本化管理**：每个变更都有唯一标识符
- **自动生成**：基于模型变化自动生成迁移脚本
- **双向操作**：支持升级（upgrade）和降级（downgrade）
- **异步支持**：完美适配 FastAPI 的异步架构

### 安装与初始化

**1. 安装 Alembic**

```bash
uv add alembic
```

**2. 初始化异步环境**
```bash
alembic init -t async alembic
```

关键参数解析：
- `-t async`：使用异步模板，适配我们的 `AsyncSession`
- `alembic`：创建的配置目录名（业界标准约定）

**3. 目录结构**
```
fastapi-demo-project/
├── alembic/
│   ├── versions/          # 迁移脚本存放目录
│   ├── env.py            # 环境配置文件
│   ├── script.py.mako    # 迁移脚本模板
│   └── README
├── alembic.ini           # 主配置文件
└── ...

```

### 配置 env.py：连接模型与数据库

```python
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context


# ----------------- 我们改造的起点 -----------------
import os
import sys
from pathlib import Path

# 步骤1：将项目根目录加入 Python 的模块搜索路径
# 这确保了 Alembic 能找到我们 app 目录下的代码
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# 步骤2：动态加载 .env 文件，让配置与环境同步
# 这让我们可以用类似 `ENVIRONMENT=prod alembic upgrade head` 的方式来操作不同数据库
ENV = os.getenv("ENVIRONMENT", "dev")
dotenv_file = project_root / f".env.{ENV}"

from dotenv import load_dotenv
load_dotenv(dotenv_file)

# 步骤3：导入我们的配置和模型定义的 Base
# 这是最关键的一步，让 Alembic 知道我们的数据库在哪，以及我们的模型长什么样
from app.core.config import Settings
from app.models import Base # 这会触发 app/models/__init__.py, 进而加载所有模型

# 实例化我们的配置
settings = Settings()
# ----------------- 我们改造的终点 -----------------


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
# 这是 Alembic 的配置对象，我们将把数据库 URL 注入进去
config = context.config

# ----------------- 注入数据库 URL -----------------
# 用我们从 settings 中读取的 URL 覆盖 alembic.ini 中的默认值
config.set_main_option("sqlalchemy.url", settings.DB.DATABASE_URL)
# ----------------------------------------------------

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# 从配置文件中解释日志配置。
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# 这是 Alembic 进行比对的"最终蓝图"
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```



`env.py` 是 Alembic 的核心配置文件，负责：

- 连接数据库
- 加载模型元数据
- 配置迁移环境

**关键配置点**：

**1. 导入模型基类**

 `app/models/__init__.py` 文件会被执行，它像一个“模型登记员”，将我们所有的模型都加载了进来

```python
# alembic/env.py
from app.models import Base  # 导入我们的模型基类

# app/models/__init__.py
from .base import Base
from .users import User
from .heroes import Hero

__all__ = ["Base", "User", "Hero"]
```

**2. 设置目标元数据**

它把我们所有 SQLAlchemy 模型（继承自 `Base`）的结构信息集合——`metadata`——交给了 Alembic

Alembic 会将这份“代码里的最终蓝图”与“数据库里的实际建筑”进行比对，从而发现差异

```python
# 将 target_metadata 从 None 改为 Base.metadata
target_metadata = Base.metadata
```

**3. 数据库连接配置**

```python
# 从设置中获取数据库 URL
from app.core.settings import settings
config.set_main_option("sqlalchemy.url", settings.database_url)
```

这样配置后，Alembic 就能：
- 自动发现所有继承自 `Base` 的模型
- 比较当前模型与数据库的差异
- 生成相应的迁移脚本



### 迁移工作流：从生成到应用

**1. 生成初始迁移**
```bash
uv run alembic revision --autogenerate -m "Initial migration"
```

**命令解析**：
- `revision`：创建新的迁移版本
- `--autogenerate`：自动检测 `target_metadata` 和数据库之间的差异，并生成相应的 Python 迁移代码。
- `-m`：添加描述性消息（强烈建议使用有意义的描述）

**2. 检查生成的迁移文件**

```python
"""Initial migration

Revision ID: 736113213a43
Revises: 
Create Date: 2025-08-23 04:07:49.727670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '736113213a43'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('heroes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('alias', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_heroes_alias'), 'heroes', ['alias'], unique=True)
    op.create_index(op.f('ix_heroes_id'), 'heroes', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_created_at'), 'users', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_created_at'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_heroes_id'), table_name='heroes')
    op.drop_index(op.f('ix_heroes_alias'), table_name='heroes')
    op.drop_table('heroes')
    # ### end Alembic commands ###

```

**3. 应用迁移**

```bash
# 升级到最新版本：这条命令会运行刚才生成的迁移脚本中的 upgrade() 函数。
uv run alembic upgrade head

# 查看当前版本
uv run alembic current

# 查看迁移历史
uv run alembic history --verbose
```

首次迁移执行成功后，会发现数据库中多了一个陌生的 `alembic_version` 表。它里面只存一行数据，记录了当前数据库已经应用到的最新迁移版本的 ID，每次你运行 `upgrade` 或 `downgrade`，Alembic 都会先查这个表，来确定自己应该从哪个版本开始工作，并将最终的版本号记录下来。这保证了迁移操作绝不会重复执行，安全可靠。



### 实战演示：为 Hero 添加 powers 字段

让我们通过一个完整的例子，演示如何安全地为现有模型添加新字段。

**场景**：为 `Hero` 模型添加 `powers` 字段来描述英雄能力

**步骤 1：修改模型定义**
```python
# app/models/heroes.py
from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Hero(Base):
    __tablename__ = "heroes"
    # 一个英雄的表，包含了名字以及称号两个字段
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    alias: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    # 💡 新增一个 powers 字段，注意它必须是可选的！
    powers: Mapped[str | None] = mapped_column(Text, nullable=True) # 使用Text可以存储更长的文本

    def __repr__(self) -> str:
        return f"<Hero(id={self.id!r}, name={self.name!r}, alias={self.alias!r})>"
```

**步骤 2：生成迁移脚本**
```bash
uv run alembic revision --autogenerate -m "Add powers field to Hero model"
```

**步骤 3：检查生成的迁移**
```python
"""Add powers column to heroes table

Revision ID: 309a4ffb61af
Revises: 736113213a43
Create Date: 2025-08-23 04:10:37.137010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '309a4ffb61af'
down_revision: Union[str, Sequence[str], None] = '736113213a43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('heroes', sa.Column('powers', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('heroes', 'powers')
    # ### end Alembic commands ###

```

**步骤 4：应用迁移**
```bash
# 先在开发环境测试
uv run alembic upgrade head

# 验证结果
uv run alembic current
```





**步骤 5：回退版本**
如果你发现这次升级有问题，可以使用Alembic撤销它？ 

```python
uv run alembic downgrade -1
```

`downgrade -1` 意味着“回退一个版本”。执行它，Alembic 会找到上一个版本的迁移脚本，并执行里面的 `downgrade()` 函数，在这里就是删除 `powers` 字段，同时更新 `alembic_version` 表。就像这次变更从未发生过一样！

- 如果想一次回退 N 个版本，用 `-N`，例如 `-2`。
- 也可以直接指定目标 revision 号：`alembic downgrade <revision_id>`。



### 常用命令速查

```bash
# 基础操作
uv run alembic current                    # 查看当前版本
uv run alembic history --verbose          # 详细历史
uv run alembic show <revision>            # 查看特定迁移

# 迁移操作
uv run alembic upgrade head              # 升级到最新
uv run alembic upgrade +1                # 升级一个版本
uv run alembic downgrade -1              # 回滚一个版本
uv run alembic downgrade base            # 回滚到初始状态

# 预览操作
uv run alembic upgrade head --sql        # 查看 SQL 不执行
uv run alembic check                     # 检查模型与数据库一致性
```

Alembic 的能力远不止于此。对于更复杂的场景，比如需要进行数据回填（给老数据的 `powers` 列填充默认值）、处理复杂的外键约束变更等，就需要我们手动去编写迁移脚本的逻辑
