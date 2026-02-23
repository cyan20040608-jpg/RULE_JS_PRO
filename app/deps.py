"""公共依赖：数据库会话与当前管理员解析。"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import SessionLocal
from app.models.admin import Admin

# 令牌读取器，供受保护接口使用。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db():
    """提供请求级别的数据库会话。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_admin(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Admin:
    """根据令牌解析并校验当前管理员。"""
    admin_id = decode_access_token(token)
    if not admin_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    admin = db.query(Admin).filter(Admin.id == int(admin_id), Admin.is_deleted == False).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return admin
