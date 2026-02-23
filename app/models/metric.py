"""指标定义与指标快照模型。"""

from sqlalchemy import JSON, Column, ForeignKey, Index, Integer, Numeric, String, Text, DateTime

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class MetricDef(Base, AuditMixin):
    """指标定义。"""
    __tablename__ = "metric_def"
    __table_args__ = mysql_table_args(
        Index("idx_metric_def_category_deleted", "metric_category", "is_deleted"),
    )

    id = Column(Integer, primary_key=True)
    metric_code = Column(String(64), nullable=False, unique=True, comment="指标编码")
    metric_name = Column(String(128), nullable=False, comment="指标名称")
    metric_category = Column(String(32), nullable=False, comment="指标类别")
    calc_rule = Column(Text, nullable=True, comment="计算规则")
    refresh_cycle = Column(String(32), nullable=True, comment="刷新周期")
    description = Column(Text, nullable=True, comment="说明")


class MetricSnapshot(Base, AuditMixin):
    """指标快照数据。"""
    __tablename__ = "metric_snapshot"
    __table_args__ = mysql_table_args(
        Index("idx_metric_snapshot_metric_time_deleted", "metric_id", "stat_time", "is_deleted"),
    )

    id = Column(Integer, primary_key=True)
    metric_id = Column(
        Integer,
        ForeignKey("metric_def.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="指标",
    )
    metric_value = Column(Numeric(18, 4), nullable=False, default=0, comment="指标值")
    stat_time = Column(DateTime, nullable=False, comment="统计时间")
    dimension_json = Column(JSON, nullable=True, comment="维度信息")
