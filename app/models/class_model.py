from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.sql.elements import quoted_name

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class Class(Base, AuditMixin):
    # "class" is a reserved keyword, so force quoted table name for MySQL.
    __tablename__ = quoted_name("class", True)
    __table_args__ = mysql_table_args(
        Index("idx_class_major_grade_deleted", "major_id", "grade_year", "is_deleted"),
        Index("idx_class_head_teacher", "head_teacher_id"),
    )

    id = Column(Integer, primary_key=True)
    class_name = Column(String(128), nullable=False, comment="班级名称")
    class_code = Column(String(64), nullable=False, unique=True, comment="班级编码")
    major_id = Column(
        Integer,
        ForeignKey("major.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="所属专业",
    )
    grade_year = Column(Integer, nullable=False, comment="入学年份")
    head_teacher_id = Column(
        Integer,
        ForeignKey("teacher.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        comment="班主任教师",
    )
    student_count = Column(Integer, nullable=False, default=0, comment="班级人数")
