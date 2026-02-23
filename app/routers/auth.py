"""认证路由：登录与登出接口。"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import authenticate_admin

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """管理员登录，返回访问令牌。"""
    token = authenticate_admin(db, payload.username, payload.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    res = TokenResponse()
    res.access_token = token
    return res


@router.post("/logout")
def logout():
    """管理员登出（当前为无状态占位实现）。"""
    return {"message": "ok"}
