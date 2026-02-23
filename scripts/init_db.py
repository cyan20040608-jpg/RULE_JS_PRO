"""数据库初始化脚本：建表、结构校验与简单查询校验。"""

import os
import sys

from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError, ProgrammingError, SQLAlchemyError

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.db.base import Base
from app.db.session import SessionLocal, engine

# 先导入全部模型，确保元数据能拿到所有表映射。
import app.models  # noqa: F401


EXPECTED_TABLES = {
    "admin",
    "college",
    "major",
    "class",
    "student",
    "teacher",
    "course",
    "course_class",
    "enroll",
    "score",
    "attendance",
    "classroom",
    "metric_def",
    "metric_snapshot",
    "alert_rule",
    "alert_event",
    "chat_history",
    "workflow_log",
    "sql_log",
    "strategy_policy",
    "query_template",
    "audit_log",
    "system_config",
}


def init_db() -> None:
    """创建所有尚不存在的表。"""
    Base.metadata.create_all(bind=engine, checkfirst=True)


def verify_tables(expected_tables: set[str]) -> None:
    """校验目标表是否全部创建成功。"""
    inspector = inspect(engine)
    actual_tables = set(inspector.get_table_names())
    missing_tables = sorted(expected_tables - actual_tables)
    if missing_tables:
        raise RuntimeError(f"Missing tables: {', '.join(missing_tables)}")

    print(f"Table verification passed: {len(expected_tables)} tables")


def verify_schema_details() -> None:
    """校验关键外键与索引是否存在。"""
    inspector = inspect(engine)

    major_fk_targets = {fk["referred_table"] for fk in inspector.get_foreign_keys("major")}
    if "college" not in major_fk_targets:
        raise RuntimeError("Schema verification failed: major.college_id foreign key missing")

    class_fk_targets = {fk["referred_table"] for fk in inspector.get_foreign_keys("class")}
    if "major" not in class_fk_targets or "teacher" not in class_fk_targets:
        raise RuntimeError("Schema verification failed: class foreign keys missing")

    student_indexes = {idx["name"] for idx in inspector.get_indexes("student")}
    if "idx_student_class_status_deleted" not in student_indexes:
        raise RuntimeError("Schema verification failed: student index missing")

    print("Schema detail verification passed")


def smoke_query() -> None:
    """执行最小查询，验证连接和基础查询能力。"""
    with SessionLocal() as db:
        db.execute(text("SELECT 1"))
        db.execute(text("SELECT COUNT(*) FROM admin"))
    print("Smoke query passed")


def main() -> None:
    """脚本主入口。"""
    try:
        print("Initializing database schema...")
        init_db()
        verify_tables(EXPECTED_TABLES)
        verify_schema_details()
        smoke_query()
        print("Database initialization completed")
    except (OperationalError, ProgrammingError) as exc:
        print(f"[DB ERROR] {exc.__class__.__name__}: {exc}")
        sys.exit(1)
    except SQLAlchemyError as exc:
        print(f"[SQLAlchemy ERROR] {exc.__class__.__name__}: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"[INIT ERROR] {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
