"""系统配置模型。"""

from sqlalchemy import Column, Index, Integer, String, Text

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class SystemConfig(Base, AuditMixin):
    """系统键值配置。"""
    __tablename__ = "system_config"
    __table_args__ = mysql_table_args(
        Index("idx_system_config_deleted_updated", "is_deleted", "updated_at"),
    )

    id = Column(Integer, primary_key=True)
    config_key = Column(String(128), nullable=False, unique=True, comment="配置键")
    config_value = Column(Text, nullable=False, comment="配置值")
    description = Column(Text, nullable=True, comment="配置说明")
