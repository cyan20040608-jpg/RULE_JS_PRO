from sqlalchemy import JSON, Column, Index, Integer, String, Text

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class WorkflowLog(Base, AuditMixin):
    __tablename__ = "workflow_log"
    __table_args__ = mysql_table_args(
        Index("idx_workflow_log_session_step_created", "session_id", "step_name", "created_at"),
        Index("idx_workflow_log_status_risk_created", "status", "risk_level", "created_at"),
    )

    id = Column(Integer, primary_key=True)
    session_id = Column(String(128), nullable=False, comment="会话编号")
    step_name = Column(String(64), nullable=False, comment="步骤名称")
    input_json = Column(JSON, nullable=True, comment="步骤输入")
    output_json = Column(JSON, nullable=True, comment="步骤输出")
    status = Column(String(20), nullable=False, comment="执行状态")
    error_message = Column(Text, nullable=True, comment="错误信息")
    risk_level = Column(String(16), nullable=True, comment="风险等级")
