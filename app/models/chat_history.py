from sqlalchemy import Column, ForeignKey, Index, Integer, String, Text

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class ChatHistory(Base, AuditMixin):
    __tablename__ = "chat_history"
    __table_args__ = mysql_table_args(
        Index("idx_chat_history_session_created", "session_id", "created_at"),
        Index("idx_chat_history_admin_created", "admin_id", "created_at"),
    )

    id = Column(Integer, primary_key=True)
    admin_id = Column(
        Integer,
        ForeignKey("admin.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        comment="管理员",
    )
    session_id = Column(String(128), nullable=False, comment="会话编号")
    message_role = Column(String(16), nullable=False, comment="角色")
    message_content = Column(Text, nullable=False, comment="消息内容")
    tokens = Column(Integer, nullable=True, comment="消耗 tokens")
    model_name = Column(String(64), nullable=True, comment="模型名称")
