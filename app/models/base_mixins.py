from sqlalchemy import Boolean, Column, DateTime, Integer, text
from sqlalchemy.sql import func


class AuditMixin:
    """Shared audit fields for all business tables."""

    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )
    created_by = Column(Integer, nullable=True, comment="创建人")
    updated_by = Column(Integer, nullable=True, comment="更新人")
    is_deleted = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("0"),
        comment="逻辑删除",
    )


def mysql_table_args(*args):
    """Attach common MySQL table options while preserving index/constraint args."""

    return (
        *args,
        {
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8mb4",
            "mysql_collate": "utf8mb4_unicode_ci",
        },
    )
