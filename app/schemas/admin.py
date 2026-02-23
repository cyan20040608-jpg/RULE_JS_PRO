"""管理员相关的数据模型。"""

from pydantic import BaseModel


class AdminProfile(BaseModel):
    """管理员个人资料返回结构。"""

    id: int
    username: str
    real_name: str | None = None
    phone: str | None = None
    email: str | None = None
    status: str

    class Config:
        # 允许从模型对象直接构建响应。
        from_attributes = True
