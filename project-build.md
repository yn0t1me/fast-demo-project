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


