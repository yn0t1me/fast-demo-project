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
