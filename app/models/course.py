"""课程模型。"""

from sqlalchemy import Column, ForeignKey, Index, Integer, Numeric, String, Text

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class Course(Base, AuditMixin):
    """课程基础信息。"""
    __tablename__ = "course"
    __table_args__ = mysql_table_args(
        Index("idx_course_college_type_deleted", "college_id", "course_type", "is_deleted"),
    )

    id = Column(Integer, primary_key=True)
    course_name = Column(String(128), nullable=False, comment="课程名称")
    course_code = Column(String(64), nullable=False, unique=True, comment="课程编码")
    credit = Column(Numeric(4, 1), nullable=False, default=0, comment="学分")
    hours = Column(Integer, nullable=False, default=0, comment="学时")
    course_type = Column(String(32), nullable=False, comment="课程类型")
    college_id = Column(
        Integer,
        ForeignKey("college.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="所属学院",
    )
    description = Column(Text, nullable=True, comment="描述")
