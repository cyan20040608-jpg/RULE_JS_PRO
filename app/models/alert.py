from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class AlertRule(Base, AuditMixin):
    __tablename__ = "alert_rule"
    __table_args__ = mysql_table_args(
        Index("idx_alert_rule_metric_status_deleted", "metric_id", "status", "is_deleted"),
        Index("idx_alert_rule_level_status", "level", "status"),
    )

    id = Column(Integer, primary_key=True)
    rule_name = Column(String(128), nullable=False, comment="规则名称")
    metric_id = Column(
        Integer,
        ForeignKey("metric_def.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="关联指标",
    )
    condition_expr = Column(Text, nullable=False, comment="触发条件")
    level = Column(String(16), nullable=False, comment="预警等级")
    action_hint = Column(Text, nullable=True, comment="处置建议")
    status = Column(String(20), nullable=False, default="enabled", comment="启用状态")


class AlertEvent(Base, AuditMixin):
    __tablename__ = "alert_event"
    __table_args__ = mysql_table_args(
        Index("idx_alert_event_time_level_status_deleted", "event_time", "level", "status", "is_deleted"),
        Index("idx_alert_event_rule_status", "rule_id", "status"),
    )

    id = Column(Integer, primary_key=True)
    rule_id = Column(
        Integer,
        ForeignKey("alert_rule.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="规则",
    )
    metric_snapshot_id = Column(
        Integer,
        ForeignKey("metric_snapshot.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="指标快照",
    )
    event_time = Column(DateTime, nullable=False, server_default=func.now(), comment="触发时间")
    level = Column(String(16), nullable=False, comment="事件等级")
    status = Column(String(20), nullable=False, default="pending", comment="处理状态")
    handler = Column(String(64), nullable=True, comment="处理人")
    handle_time = Column(DateTime, nullable=True, comment="处理时间")
    handle_note = Column(Text, nullable=True, comment="处理说明")
