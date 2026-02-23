"""配置模块：从环境变量读取应用、数据库与令牌配置。"""

import os
from datetime import timedelta
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    # 优先加载项目根目录下的环境配置文件。
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(env_path)


class Settings:
    """项目运行配置。"""

    app_name = "edu_cockpit"

    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_port = int(os.getenv("DB_PORT", "3306"))
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "edu_admin")

    jwt_secret = os.getenv("JWT_SECRET", "change_me")
    jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

    @property
    def database_url(self) -> str:
        """生成数据库连接串。"""
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"
        )

    @property
    def access_token_expires(self) -> timedelta:
        """返回访问令牌默认有效期。"""
        return timedelta(minutes=self.access_token_expire_minutes)


settings = Settings()
