# Pydantic Settings 配置管理指南

## 简介

pydantic_settings 是 Pydantic V2 中专门用于管理应用程序配置的模块，它基于强大的 Pydantic 模型验证机制，简化了配置加载和验证过程。
通过 pydantic_settings，开发者能以声明式方法管理配置，兼顾灵活性和安全性，是现代化 Python 应用的推荐配置方案。


## 安装

```bash
uv add pydantic_settings
```

## 核心组件

### BaseSettings 类

配置模型的基类，继承自 `pydantic.BaseModel`，添加了从环境变量/文件加载配置的能力：

```python
from pydantic_settings import BaseSettings
```

### SettingsConfigDict 类

替换旧版的 Config 类，用于配置模型行为，如加载环境变量相关设置、指定配置文件等（通过 model_config 属性设置）：

```python
from pydantic_settings import SettingsConfigDict
```

## 基本用法

### 定义配置模型(配置文件使用)

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    debug: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env",          # 指定从 .env 文件加载环境变量配置
        case_sensitive=False,     # 设置环境变量名不区分大小写（默认值）
        extra="ignore"            # 忽略配置文件中未在模型中定义的额外字段
    )

settings = Settings()
print(settings.database_url)
```

创建 `.env` 文件：

```env
DATABASE_URL=postgresql://user:password@localhost:5432/mydatabase
DEBUG=true
```
Pydantic Settings 会读取 .env 文件内容，将文件中的键值对加载为环境变量，按照环境变量的规则进行处理，因此它也大小写不敏感。

### 定义配置模型(环境变量使用)

```python
import os

os.environ["DEMO_APP_NAME"] = "线上系统"
os.environ["DEMO_PORT"] = "9000"

class ProdSettings(BaseSettings):
    app_name: str
    port: int
    
    model_config = SettingsConfigDict(
        env_prefix="DEMO_"  # 环境变量前缀
    )

prod = ProdSettings()
print(prod.app_name)  # 输出：线上系统
print(prod.port)      # 输出：9000
```

## 配置加载优先级

BaseSettings 按从低到高的优先级合并配置源：

1. 模型字段的默认值（如 `debug=False`）
2. 环境变量（如 `DEBUG=False`）
3. `.env` 文件中的变量
4. 显式传递的参数（如 `Settings(debug=False)`）

**注：高优先级覆盖低优先级。**

## SettingsConfigDict 关键参数

| 参数 | 说明 |
|------|------|
| `env_file` | 指定 .env 文件路径（支持 .env, .env.prod 等） |
| `env_file_encoding` | 文件编码（默认 utf-8） |
| `env_prefix` | 环境变量前缀（如 "APP_" 使 api_key → APP_API_KEY） |
| `case_sensitive` | 是否区分环境变量大小写（默认 False） |
| `env_nested_delimiter` | 嵌套模型分隔符（如 __ 可将 DB__HOST 解析到 db.host） |
| `secrets_dir` | 从 secrets 等目录加载敏感数据 |
| `extra` | 处理额外字段的策略（"allow", "ignore", "forbid"） |

## 高级特性

### 敏感数据保护

使用 `SecretStr` 或 `SecretBytes` 保护敏感信息：

```python
from pydantic import BaseModel, SecretStr

class DbConfig(BaseModel):
    host: str = 'localhost'
    port: int = 3306
    name: str = 'exam'
    user: str = 'root'
    password: SecretStr = SecretStr('123456')

db = DbConfig()
print(db.password, type(db.password))
print(db.password.get_secret_value())

# 输出结果
# ********** <class 'pydantic.types.SecretStr'>
# 123456
```

### 使用 secrets_dir 配置项

```python
class SecureSettings(BaseSettings):
    admin_password: str        # 从文件读取 secrets/admin_password
    
    model_config = SettingsConfigDict(
        secrets_dir="./secrets",  # 指定敏感数据存储目录
    )
```

admin_password 字段会自动从 ./secrets/admin_password 文件中读取内容。

### 嵌套配置模型

配置文件 `.env1`：

```env
# 应用配置
APP_DEBUG=True

# 数据库配置
APP_DB_HOST=192.168.31.112
APP_DB_PORT=3306
APP_DB_USER=root
APP_DB_PASSWORD=121212
APP_DB_NAME=test1

# redis配置
APP_REDIS_HOST=192.168.31.112
APP_REDIS_PORT=6379
```

配置模型定义：

```python
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# 数据库配置项
class DbConfig(BaseModel):
    host: str = 'localhost'
    port: int = 3306
    name: str = 'exam'
    user: str = 'root'
    password: SecretStr = SecretStr('123456')

# redis配置项
class RedisConfig(BaseModel):
    host: str = 'localhost'
    port: int = 6379

# 项目应用配置
class AppConfig(BaseSettings):
    db: DbConfig
    redis: RedisConfig
    debug: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env1",
        env_prefix="APP_",
        env_nested_delimiter='_'  # 嵌套分隔符,如 _ 可将 DB_HOST 解析到 db.host
    )

app = AppConfig()
print(app.db)
print(app.db.password.get_secret_value())
print(app.redis)
```

映射规则：

- APP_DB_HOST → db.host
- APP_DB_PORT → db.port
- APP_REDIS_HOST → redis.host
- APP_DEBUG → debug

### 多环境配置

```python
class Config(BaseSettings):
    env: str = "dev"
    
    # 根据 env 动态加载 .env.{env} 文件
    model_config = SettingsConfigDict(
        env_file=".env.{env}",
        env_file_encoding="utf-8"
    )

# 启动时设置环境变量：export ENV=prod
```

### 配置校验

要是配置项有特殊要求，可以添加验证函数：

```python
from pydantic import field_validator

@field_validator("port")
@classmethod
def check_port(cls, v):
    if not 1024 <= v <= 65535:
        raise ValueError("端口号得在1024到65535之间")
    return v
```

### 不同环境配置管理

```python
class DevSettings(BaseSettings):
    env: str = "dev"
    debug: bool = True

class ProdSettings(BaseSettings):
    env: str = "prod"
    debug: bool = False

# 根据环境变量选择配置
settings = DevSettings() if os.getenv("ENV") == "dev" else ProdSettings()
```

## 最佳实践

1. **敏感字段**：使用 `pydantic.SecretStr` 或 `SecretBytes` 避免日志泄露。

2. **环境隔离**：通过 `env` 参数区分开发/生产配置（如 `.env.dev`, `.env.prod`）。

3. **类型安全**：为所有字段指定类型（如 `int`, `bool`），Pydantic 会自动转换类型。

4. **前缀规范**：为不同应用设置 `env_prefix` 防止环境变量冲突。

5. **类型标注**：类里面定义的每个变量都得标注类型，这样 PyDantic 才能帮你检查值的类型对不对。

## 常见错误处理

1. **缺失必填字段**：抛出 `ValidationError`，检查环境变量名是否正确。

2. **类型转换失败**：如非数字赋给 `int` 字段，抛出类型错误。

3. **文件加载失败**：忽略错误（除非文件显式指定），确保文件存在且路径正确。

## 总结

Pydantic Settings 让配置管理变得超级规范，自带类型检查，配合环境变量使用非常方便。配置文件不再是个随便写写的 dict，而是个规范的配置类。有了这个工具，配置管理轻轻松松！
通过 pydantic_settings，开发者能以声明式方法管理配置，兼顾灵活性和安全性，是现代化 Python 应用的推荐配置方案。
