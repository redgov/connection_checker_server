from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from src.db_setting import ModelBase


class MailAddressModel(ModelBase):
    """MailAddressInfo
    """

    __tablename__ = 'mail_addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False)
    mail_address_to_group = relationship("MailAddressToGroupModel")

    def __init__(self, address: str):
        self.address = address
