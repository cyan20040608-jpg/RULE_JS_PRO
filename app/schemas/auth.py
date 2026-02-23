"""认证相关的数据模型。"""

from pydantic import BaseModel


class LoginRequest(BaseModel):
    """登录请求体。"""

    username: str
    password: str


class TokenResponse(BaseModel):
    """登录成功返回的令牌结构。"""

    access_token: str
    token_type: str = "bearer"
