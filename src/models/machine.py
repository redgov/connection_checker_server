from datetime import datetime
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    Boolean,
    DateTime,
)
from src.db_setting import ModelBase, Session


session = Session()


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

    def __init__(self,
                 group_id: int,
                 name: str,
                 ip_address: str,
                 is_active: bool = True):
        self.group_id = group_id
        self.name = name
        self.ip_address = ip_address
        self.is_active = is_active

    @classmethod
    def get(cls):
        machines = session.query(cls).order_by(cls.id).all()
        return machines

    @classmethod
    def save(cls, group_id: int, name: str, ip_address: str):
        machine = cls(group_id, name, ip_address)
        session.add(machine)

    @classmethod
    def update(cls,
               machine_id: int,
               group_id: int,
               name: str,
               address: str,
               is_active: bool) -> None:

        machine = session.query(cls).filter(cls.id == machine_id).scalar()
        machine.group_id = group_id
        machine.name = name
        machine.ip_address = address
        machine.is_active = is_active

    @classmethod
    def delete(cls, id: int) -> None:
        session.query(cls).filter(cls.id == id).delete()
