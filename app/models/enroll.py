from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class Enroll(Base, AuditMixin):
    __tablename__ = "enroll"
    __table_args__ = mysql_table_args(
        UniqueConstraint("student_id", "course_class_id", name="uq_enroll_student_course_class"),
        Index("idx_enroll_course_class_status_deleted", "course_class_id", "status", "is_deleted"),
    )

    id = Column(Integer, primary_key=True)
    student_id = Column(
        Integer,
        ForeignKey("student.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="学生",
    )
    course_class_id = Column(
        Integer,
        ForeignKey("course_class.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="教学班",
    )
    enroll_time = Column(DateTime, nullable=False, server_default=func.now(), comment="选课时间")
    status = Column(String(20), nullable=False, default="selected", comment="选课状态")
