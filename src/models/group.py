from typing import Set
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
    def get(cls):

        models = session.query(cls.id, cls.name, MailAddressModel.address). \
            outerjoin(MailAddressToGroupModel,
                      cls.id == MailAddressToGroupModel.group_id). \
            outerjoin(MailAddressModel,
                      MailAddressToGroupModel.address_id == MailAddressModel.id). \
            order_by(cls.id)

        groups = []
        group = {}
        now_group_id = None

        for m in models:
            if now_group_id != m.id:

                if now_group_id != None:
                    groups.append(group)

                now_group_id = m.id
                group = {"id": m.id, "name": m.name,
                         "addresses": ""}

            if m.address != None:
                group["addresses"] += f"{m.address}\r\n"
        if group != {}:
        groups.append(group)  # 最後のグループもちゃんと追加

        return groups

    @classmethod
    def save(cls, name: str, mail_addresses: Set[str]) -> None:

        group_model = cls(name)
        session.add(group_model)

        saved_address_models = session.query(MailAddressModel.id,
                                             MailAddressModel.address). \
            filter(MailAddressModel.address.in_(mail_addresses)). \
            all()

        saved_addresses = {m.address for m in saved_address_models}
        new_mail_addresses = list(mail_addresses - saved_addresses)

        mail_address_models = [
            MailAddressModel(address)
            for address in new_mail_addresses
        ]
        session.add_all(mail_address_models)
        session.flush()

        mail_address_to_group_models = [
            MailAddressToGroupModel(address_model.id, group_model.id)
            for address_model in mail_address_models
        ]
        session.add_all(mail_address_to_group_models)

        mail_address_to_group_models = [
            MailAddressToGroupModel(address.id, group_model.id)
            for address in saved_addresses
        ]
        session.add_all(mail_address_to_group_models)

    @classmethod
    def delete(cls, id: int) -> None:

        session.query(MailAddressToGroupModel). \
            filter(MailAddressToGroupModel.group_id == id).\
            delete()

        session.query(cls). \
            filter(cls.id == id). \
            delete()
