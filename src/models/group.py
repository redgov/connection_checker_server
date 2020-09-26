from typing import List
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from src.db_setting import ModelBase, Session
from src.models.mail_address import MailAddressModel
from src.models.mail_address_to_group import MailAddressToGroupModel


session = Session()


class GroupModel(ModelBase):
    """GroupInfo
    """

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False)
    machines = relationship("MachineModel")
    mail_address_to_group = relationship("MailAddressToGroupModel")

    def __init__(self, name: str):
        self.name = name

    @classmethod
    def save(cls, name: str, mail_addresses: List[str]) -> None:
        
        group_model = cls(name)
        session.add(group_model)

        mail_address_models = [
            MailAddressModel(address)
            for address in mail_addresses
        ]
        session.add_all(mail_address_models)
        session.flush()

        mail_address_to_group_models = [
            MailAddressToGroupModel(address_model.id, group_model.id)
            for address_model in mail_address_models 
        ]
        session.add_all(mail_address_to_group_models)
