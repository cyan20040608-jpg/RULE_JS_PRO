"""考勤记录模型。"""

from sqlalchemy import Column, Date, ForeignKey, Index, Integer, String, UniqueConstraint

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class Attendance(Base, AuditMixin):
    """学生考勤记录。"""
    __tablename__ = "attendance"
    __table_args__ = mysql_table_args(
        UniqueConstraint(
            "student_id",
            "course_class_id",
            "attend_date",
            name="uq_attendance_student_class_date",
        ),
        Index(
            "idx_attendance_class_date_status_deleted",
            "course_class_id",
            "attend_date",
            "status",
            "is_deleted",
        ),
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
    attend_date = Column(Date, nullable=False, comment="日期")
    status = Column(String(20), nullable=False, comment="出勤状态")
