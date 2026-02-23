"""认证服务：处理管理员登录鉴权流程。"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.models.admin import Admin


def authenticate_admin(db: Session, username: str, password: str) -> str | None:
    """校验管理员账号密码，成功则返回访问令牌。"""
    admin = db.query(Admin).filter(Admin.username == username, Admin.is_deleted == False).first()
    if not admin:
        return None
    if not verify_password(password, admin.password_hash):
        return None

    # 记录最近一次登录时间。
    admin.last_login_at = datetime.utcnow()
    db.add(admin)
    db.commit()

    return create_access_token(subject=str(admin.id))
