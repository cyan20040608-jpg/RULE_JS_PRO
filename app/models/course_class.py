from sqlalchemy import Column, ForeignKey, Index, Integer, String, Text

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class CourseClass(Base, AuditMixin):
    __tablename__ = "course_class"
    __table_args__ = mysql_table_args(
        Index("idx_course_class_term_course_class_deleted", "term", "course_id", "class_id", "is_deleted"),
        Index("idx_course_class_teacher_term_deleted", "teacher_id", "term", "is_deleted"),
    )

    id = Column(Integer, primary_key=True)
    course_id = Column(
        Integer,
        ForeignKey("course.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="课程",
    )
    class_id = Column(
        Integer,
        ForeignKey("class.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="班级",
    )
    teacher_id = Column(
        Integer,
        ForeignKey("teacher.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="授课教师",
    )
    term = Column(String(32), nullable=False, comment="学期")
    schedule_info = Column(Text, nullable=True, comment="上课时间地点")
    max_students = Column(Integer, nullable=False, default=0, comment="最大人数")
