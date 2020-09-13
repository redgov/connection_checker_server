from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from src.db_setting import ModelBase


class GroupModel(ModelBase):
    """GroupInfo
    """

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False)
    machines = relationship("MachineModel")
    mail_address_to_machine = relationship("MailAddressToMachineModel")
