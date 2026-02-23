"""查询模板模型。"""

from sqlalchemy import JSON, Column, Index, Integer, String, Text

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class QueryTemplate(Base, AuditMixin):
    """可复用查询模板。"""
    __tablename__ = "query_template"
    __table_args__ = mysql_table_args(
        Index("idx_query_template_status_created", "status", "created_at"),
    )

    id = Column(Integer, primary_key=True)
    template_name = Column(String(128), nullable=False, unique=True, comment="模板名称")
    template_desc = Column(Text, nullable=True, comment="模板说明")
    template_sql = Column(Text, nullable=False, comment="模板 SQL")
    params_schema = Column(JSON, nullable=True, comment="参数结构")
    source_session_id = Column(String(128), nullable=True, comment="来源会话")
    status = Column(String(20), nullable=False, default="enabled", comment="启用状态")
