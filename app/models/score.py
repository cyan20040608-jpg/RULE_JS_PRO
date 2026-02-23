"""成绩记录模型。"""

from sqlalchemy import Column, ForeignKey, Index, Integer, Numeric, String, UniqueConstraint

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class Score(Base, AuditMixin):
    """学生课程成绩。"""
    __tablename__ = "score"
    __table_args__ = mysql_table_args(
        UniqueConstraint("student_id", "course_class_id", "term", name="uq_score_student_class_term"),
        Index("idx_score_course_term_deleted", "course_id", "term", "is_deleted"),
        Index("idx_score_course_class_term_deleted", "course_class_id", "term", "is_deleted"),
    )

    id = Column(Integer, primary_key=True)
    student_id = Column(
        Integer,
        ForeignKey("student.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="学生",
    )
    course_id = Column(
        Integer,
        ForeignKey("course.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="课程",
    )
    course_class_id = Column(
        Integer,
        ForeignKey("course_class.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="教学班",
    )
    term = Column(String(32), nullable=False, comment="学期")
    score_value = Column(Numeric(6, 2), nullable=False, default=0, comment="成绩")
    score_level = Column(String(32), nullable=True, comment="成绩等级")
