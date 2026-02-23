"""学院模型。"""

from sqlalchemy import Column, Index, Integer, String, Text

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class College(Base, AuditMixin):
    """学院基础信息。"""
    __tablename__ = "college"
    __table_args__ = mysql_table_args(
        Index("idx_college_name", "college_name"),
        Index("idx_college_is_deleted", "is_deleted"),
    )

    id = Column(Integer, primary_key=True)
    college_name = Column(String(128), nullable=False, comment="学院名称")
    college_code = Column(String(64), nullable=False, unique=True, comment="学院编码")
    description = Column(Text, nullable=True, comment="描述")
