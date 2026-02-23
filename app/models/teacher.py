"""教师模型。"""

from sqlalchemy import Column, ForeignKey, Index, Integer, String, Date

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class Teacher(Base, AuditMixin):
    """教师基础信息。"""
    __tablename__ = "teacher"
    __table_args__ = mysql_table_args(
        Index("idx_teacher_college_status_deleted", "college_id", "status", "is_deleted"),
    )

    id = Column(Integer, primary_key=True)
    teacher_no = Column(String(64), nullable=False, unique=True, comment="工号")
    real_name = Column(String(64), nullable=False, comment="姓名")
    gender = Column(String(16), nullable=True, comment="性别")
    id_card = Column(String(32), nullable=True, unique=True, comment="身份证号")
    birth_date = Column(Date, nullable=True, comment="出生日期")
    phone = Column(String(32), nullable=True, comment="手机号")
    email = Column(String(128), nullable=True, comment="邮箱")
    title = Column(String(64), nullable=True, comment="职称")
    college_id = Column(
        Integer,
        ForeignKey("college.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="所属学院",
    )
    status = Column(String(20), nullable=False, default="active", comment="状态")
