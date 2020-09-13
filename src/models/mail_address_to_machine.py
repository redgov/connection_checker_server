from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    String, 
    Integer, 
    Boolean, 
    DateTime,
)
from sqlalchemy.orm import relationship

from src.db_setting import ModelBase


class MailAddressToMachineModel(ModelBase):
    """MailAddressToMachineInfo
    """

    __tablename__ = 'mail_address_to_machine'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address_id = Column(Integer,
                        ForeignKey("mail_addresses.id"),
                        nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False)
