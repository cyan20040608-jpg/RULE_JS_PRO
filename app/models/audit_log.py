"""操作审计日志模型。"""

from sqlalchemy import JSON, Column, ForeignKey, Index, Integer, String

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class AuditLog(Base, AuditMixin):
    """管理员操作审计日志。"""
    __tablename__ = "audit_log"
    __table_args__ = mysql_table_args(
        Index("idx_audit_log_admin_action_created", "admin_id", "action_type", "created_at"),
        Index("idx_audit_log_risk_created", "risk_level", "created_at"),
    )

    id = Column(Integer, primary_key=True)
    admin_id = Column(
        Integer,
        ForeignKey("admin.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="管理员",
    )
    action_type = Column(String(32), nullable=False, comment="操作类型")
    action_target = Column(String(128), nullable=False, comment="操作对象")
    before_json = Column(JSON, nullable=True, comment="变更前数据")
    after_json = Column(JSON, nullable=True, comment="变更后数据")
    risk_level = Column(String(16), nullable=True, comment="风险等级")
