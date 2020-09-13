from datetime import datetime
from sqlalchemy import (
    Column,
    ForeignKey,
    String, 
    Integer, 
    Boolean, 
    DateTime,
)
from src.db_setting import ModelBase


class MachineModel(ModelBase):
    """MachineInfo
    """

    __tablename__ = 'machines'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    ip_address = Column(String(50), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    is_success_last = Column(Boolean, nullable=True)
    success_time = Column(DateTime, nullable=True)
    failure_time = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False)
