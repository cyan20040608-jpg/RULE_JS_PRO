"""专业模型。"""

from sqlalchemy import Column, ForeignKey, Index, Integer, String, Text

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class Major(Base, AuditMixin):
    """专业基础信息。"""
    __tablename__ = "major"
    __table_args__ = mysql_table_args(
        Index("idx_major_college_deleted", "college_id", "is_deleted"),
        Index("idx_major_degree_type", "degree_type"),
    )

    id = Column(Integer, primary_key=True)
    major_name = Column(String(128), nullable=False, comment="专业名称")
    major_code = Column(String(64), nullable=False, unique=True, comment="专业编码")
    college_id = Column(
        Integer,
        ForeignKey("college.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="所属学院",
    )
    degree_type = Column(String(32), nullable=False, comment="学历类型")
    description = Column(Text, nullable=True, comment="描述")
