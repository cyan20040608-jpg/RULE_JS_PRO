from sqlalchemy import Column, DateTime, Index, Integer, String

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class Admin(Base, AuditMixin):
    __tablename__ = "admin"
    __table_args__ = mysql_table_args(
        Index("idx_admin_status_deleted", "status", "is_deleted"),
    )

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False, comment="账号")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    real_name = Column(String(64), nullable=True, comment="姓名")
    phone = Column(String(32), nullable=True, comment="手机号")
    email = Column(String(128), nullable=True, comment="邮箱")
    last_login_at = Column(DateTime, nullable=True, comment="最后登录时间")
    status = Column(String(20), nullable=False, default="active", comment="状态")
