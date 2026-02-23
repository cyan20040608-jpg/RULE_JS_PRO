"""数据库会话与引擎初始化。"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 创建数据库引擎，启用连接预检测避免陈旧连接问题。
engine = create_engine(settings.database_url, pool_pre_ping=True)

# 项目统一使用的会话工厂。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
