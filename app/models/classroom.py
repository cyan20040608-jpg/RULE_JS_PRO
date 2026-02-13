from sqlalchemy import Column, Index, Integer, String, UniqueConstraint

from app.db.base import Base
from app.models.base_mixins import AuditMixin, mysql_table_args


class Classroom(Base, AuditMixin):
    __tablename__ = "classroom"
    __table_args__ = mysql_table_args(
        UniqueConstraint("building", "room_no", name="uq_classroom_building_room"),
        Index("idx_classroom_status_capacity", "status", "capacity"),
    )

    id = Column(Integer, primary_key=True)
    building = Column(String(64), nullable=False, comment="教学楼")
    room_no = Column(String(64), nullable=False, comment="教室编号")
    capacity = Column(Integer, nullable=False, default=0, comment="容量")
    status = Column(String(20), nullable=False, default="available", comment="状态")
