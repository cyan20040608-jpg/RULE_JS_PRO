"""数据语句执行日志模型。"""

from sqlalchemy import JSON, Column, Index, Integer, String, Text

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class SQLLog(Base, AuditMixin):
    """查询与变更语句执行日志。"""
    __tablename__ = "sql_log"
    __table_args__ = mysql_table_args(
        Index("idx_sql_log_session_created", "session_id", "created_at"),
        Index("idx_sql_log_status_risk_created", "status", "risk_level", "created_at"),
    )

    id = Column(Integer, primary_key=True)
    session_id = Column(String(128), nullable=False, comment="会话编号")
    sql_text = Column(Text, nullable=False, comment="SQL 语句")
    params_json = Column(JSON, nullable=True, comment="SQL 参数")
    exec_time_ms = Column(Integer, nullable=True, comment="执行耗时毫秒")
    row_count = Column(Integer, nullable=True, comment="影响行数")
    status = Column(String(20), nullable=False, comment="执行状态")
    error_message = Column(Text, nullable=True, comment="错误信息")
    risk_level = Column(String(16), nullable=True, comment="风险等级")
