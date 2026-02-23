"""模型基类定义。"""

from sqlalchemy.orm import declarative_base

# 全部模型都应继承该基类对象。
Base = declarative_base()
