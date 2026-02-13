from sqlalchemy import Column, Date, ForeignKey, Index, Integer, String, Text

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class Student(Base, AuditMixin):
    __tablename__ = "student"
    __table_args__ = mysql_table_args(
        Index("idx_student_class_status_deleted", "class_id", "status", "is_deleted"),
        Index("idx_student_major_deleted", "major_id", "is_deleted"),
        Index("idx_student_college_deleted", "college_id", "is_deleted"),
    )

    id = Column(Integer, primary_key=True)
    student_no = Column(String(64), nullable=False, unique=True, comment="学号")
    real_name = Column(String(64), nullable=False, comment="姓名")
    gender = Column(String(16), nullable=True, comment="性别")
    id_card = Column(String(32), nullable=True, unique=True, comment="身份证号")
    birth_date = Column(Date, nullable=True, comment="出生日期")
    phone = Column(String(32), nullable=True, comment="手机号")
    email = Column(String(128), nullable=True, comment="邮箱")
    address = Column(Text, nullable=True, comment="家庭住址")
    class_id = Column(
        Integer,
        ForeignKey("class.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="所属班级",
    )
    major_id = Column(
        Integer,
        ForeignKey("major.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="所属专业",
    )
    college_id = Column(
        Integer,
        ForeignKey("college.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="所属学院",
    )
    enroll_year = Column(Integer, nullable=False, comment="入学年份")
    status = Column(String(20), nullable=False, default="active", comment="学籍状态")
