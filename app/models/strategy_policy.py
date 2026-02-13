from sqlalchemy import JSON, Column, Index, Integer, String, Text

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class StrategyPolicy(Base, AuditMixin):
    __tablename__ = "strategy_policy"
    __table_args__ = mysql_table_args(
        Index("idx_strategy_policy_type_status_deleted", "policy_type", "status", "is_deleted"),
    )

    id = Column(Integer, primary_key=True)
    policy_name = Column(String(128), nullable=False, unique=True, comment="策略名称")
    policy_type = Column(String(32), nullable=False, comment="策略类型")
    policy_rule = Column(JSON, nullable=False, comment="策略规则")
    status = Column(String(20), nullable=False, default="enabled", comment="启用状态")
    description = Column(Text, nullable=True, comment="策略说明")
