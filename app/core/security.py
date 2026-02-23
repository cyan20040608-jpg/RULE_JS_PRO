"""安全模块：密码哈希与令牌编解码。"""

from datetime import datetime
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# 统一密码哈希上下文。
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """对明文密码进行哈希。"""
    return _pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """校验明文密码与哈希值是否匹配。"""
    return _pwd_context.verify(plain_password, password_hash)


def create_access_token(subject: str, expires_delta=None) -> str:
    """创建访问令牌，默认使用全局配置的过期时间。"""
    expire = datetime.utcnow() + (expires_delta or settings.access_token_expires)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> Optional[str]:
    """解析访问令牌，返回主体字段（管理员编号）。"""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload.get("sub")
    except JWTError:
        return None
