"""基础表通用 CRUD 路由。"""

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.response import success_response
from app.deps import get_current_admin, get_db
from app.models.admin import Admin
from app.models.class_model import Class
from app.models.college import College
from app.models.course import Course
from app.models.major import Major
from app.models.student import Student
from app.models.teacher import Teacher

router = APIRouter()


MODEL_MAP = {
    "admin": Admin,
    "college": College,
    "major": Major,
    "class": Class,
    "student": Student,
    "teacher": Teacher,
    "course": Course,
}

PROTECTED_FIELDS = {"id", "created_at", "updated_at", "created_by", "updated_by", "is_deleted"}
RESERVED_QUERY_KEYS = {"page", "page_size"}


def _get_model(table: str):
    """根据表名获取模型，限制在白名单范围内。"""
    model = MODEL_MAP.get(table)
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"不支持的表: {table}",
        )
    return model


def _model_columns(model) -> dict[str, Any]:
    """获取模型字段名到字段对象的映射。"""
    return {column.name: column for column in model.__table__.columns}


def _parse_bool(raw: Any) -> bool:
    """将常见布尔字符串转为布尔值。"""
    if isinstance(raw, bool):
        return raw
    if isinstance(raw, (int, float)):
        return bool(raw)
    if isinstance(raw, str):
        text = raw.strip().lower()
        if text in {"1", "true", "yes", "y", "on"}:
            return True
        if text in {"0", "false", "no", "n", "off"}:
            return False
    raise ValueError(f"无法解析布尔值: {raw}")


def _parse_datetime(raw: str) -> datetime:
    """解析 ISO 格式时间字符串。"""
    return datetime.fromisoformat(raw)


def _parse_date(raw: str) -> date:
    """解析 ISO 格式日期字符串。"""
    return date.fromisoformat(raw)


def _coerce_value(column, raw: Any) -> Any:
    """按字段类型转换输入值，避免隐式脏数据写入。"""
    if raw is None:
        return None

    try:
        python_type = column.type.python_type
    except Exception:
        return raw

    try:
        if python_type is bool:
            return _parse_bool(raw)
        if python_type is int:
            return int(raw)
        if python_type is float:
            return float(raw)
        if python_type is Decimal:
            return Decimal(str(raw))
        if python_type is datetime and isinstance(raw, str):
            return _parse_datetime(raw)
        if python_type is date and isinstance(raw, str):
            return _parse_date(raw)
        return raw
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"字段 {column.name} 类型不正确: {exc}",
        ) from exc


def _serialize_row(row) -> dict[str, Any]:
    """将 ORM 对象序列化为可返回的字典。"""
    result: dict[str, Any] = {}
    for column in row.__table__.columns:
        value = getattr(row, column.name)
        if isinstance(value, (date, datetime)):
            result[column.name] = value.isoformat()
        elif isinstance(value, Decimal):
            result[column.name] = float(value)
        else:
            result[column.name] = value
    return result


def _build_filters(model, query_params: dict[str, str]):
    """构造列表查询过滤条件，默认排除逻辑删除数据。"""
    columns = _model_columns(model)
    filters = []

    for key, raw_value in query_params.items():
        if key in RESERVED_QUERY_KEYS:
            continue
        if key not in columns:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"不支持的过滤字段: {key}",
            )
        column = columns[key]
        filters.append(column == _coerce_value(column, raw_value))

    if "is_deleted" in columns and "is_deleted" not in query_params:
        filters.append(columns["is_deleted"] == False)

    return filters


def _get_item_or_404(db: Session, model, item_id: int):
    """按主键查询单条数据，不存在时抛出 404。"""
    columns = _model_columns(model)
    query = db.query(model).filter(columns["id"] == item_id)
    if "is_deleted" in columns:
        query = query.filter(columns["is_deleted"] == False)
    item = query.first()
    if not item:
        raise HTTPException(status_code=404, detail="记录不存在")
    return item


def _validate_payload(model, payload: dict[str, Any], allow_empty: bool = False) -> dict[str, Any]:
    """校验创建/更新入参，只允许可写字段。"""
    if not isinstance(payload, dict):
        raise HTTPException(status_code=422, detail="请求体必须是 JSON 对象")
    if not payload and not allow_empty:
        raise HTTPException(status_code=422, detail="请求体不能为空")

    columns = _model_columns(model)
    invalid = [key for key in payload.keys() if key not in columns or key in PROTECTED_FIELDS]
    if invalid:
        raise HTTPException(status_code=422, detail=f"存在不可写字段: {', '.join(invalid)}")

    cleaned: dict[str, Any] = {}
    for key, raw_value in payload.items():
        cleaned[key] = _coerce_value(columns[key], raw_value)
    return cleaned


@router.get("/{table}/list")
def list_items(
    table: str,
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    """分页查询指定基础表数据，并支持字段等值过滤。"""
    model = _get_model(table)
    filters = _build_filters(model, dict(request.query_params))

    query = db.query(model).filter(*filters)
    total = query.count()
    rows = (
        query.order_by(model.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    data = {
        "items": [_serialize_row(row) for row in rows],
        "page": page,
        "page_size": page_size,
        "total": total,
    }
    return success_response(data)


@router.get("/{table}/{item_id}")
def get_item(
    table: str,
    item_id: int,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    """按主键查询单条记录。"""
    model = _get_model(table)
    item = _get_item_or_404(db, model, item_id)
    return success_response(_serialize_row(item))


@router.post("/{table}")
def create_item(
    table: str,
    payload: dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """创建指定表记录。"""
    model = _get_model(table)
    cleaned = _validate_payload(model, payload)
    columns = _model_columns(model)
    if "created_by" in columns:
        cleaned["created_by"] = current_admin.id
    if "updated_by" in columns:
        cleaned["updated_by"] = current_admin.id

    row = model(**cleaned)
    db.add(row)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"数据约束冲突: {exc.orig}") from exc
    db.refresh(row)
    return success_response(_serialize_row(row), message="创建成功")


@router.put("/{table}/{item_id}")
def update_item(
    table: str,
    item_id: int,
    payload: dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """按主键更新指定表记录。"""
    model = _get_model(table)
    cleaned = _validate_payload(model, payload)
    item = _get_item_or_404(db, model, item_id)

    for key, value in cleaned.items():
        setattr(item, key, value)
    if hasattr(item, "updated_by"):
        item.updated_by = current_admin.id

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"数据约束冲突: {exc.orig}") from exc
    db.refresh(item)
    return success_response(_serialize_row(item), message="更新成功")


@router.delete("/{table}/{item_id}")
def delete_item(
    table: str,
    item_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """删除指定记录：优先逻辑删除。"""
    model = _get_model(table)
    item = _get_item_or_404(db, model, item_id)

    if hasattr(item, "is_deleted"):
        item.is_deleted = True
        if hasattr(item, "updated_by"):
            item.updated_by = current_admin.id
    else:
        db.delete(item)

    db.commit()
    return success_response({"id": item_id}, message="删除成功")
