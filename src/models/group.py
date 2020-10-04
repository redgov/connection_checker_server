from typing import Set
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from src.db_setting import ModelBase, Session
from src.models.mail_address import MailAddressModel
from src.models.mail_address_to_group import MailAddressToGroupModel
from src.models.machine import MachineModel


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
            MailAddressToGroupModel(m.id, group_model.id)
            for m in saved_address_models
        ]
        session.add_all(mail_address_to_group_models)

    @classmethod
    def update(cls, group_id: int, name: str, mail_addresses: Set[str]):

        group_model = session.query(cls).filter(cls.id == group_id).scalar()
        if group_model.name != name:
            group_model.name = name

        # 対象のグループと紐づくモデルを取得
        saved_address_models = session.query(MailAddressModel.address). \
            join(MailAddressToGroupModel,
                 MailAddressModel.id == MailAddressToGroupModel.address_id). \
            filter(MailAddressToGroupModel.group_id == group_id). \
            all()
        saved_addresses = {m.address for m in saved_address_models}

        # 編集後不要になるアドレスを削除
        addresses_target_deletion = saved_addresses - mail_addresses
        id_target_deletion = session.query(MailAddressToGroupModel.id). \
            join(MailAddressModel,
                 MailAddressModel.id == MailAddressToGroupModel.address_id). \
            filter(MailAddressToGroupModel.group_id == group_id,
                   MailAddressModel.address.in_(addresses_target_deletion)). \
            all()
        ids = [m for m in id_target_deletion]
        session.query(MailAddressToGroupModel). \
            filter(MailAddressToGroupModel.id.in_(ids)). \
            delete(synchronize_session=False)

        # 新規に追加されたアドレスをgroupと結びつける #
        saved_address_models = session.query(MailAddressModel). \
            join(MailAddressToGroupModel,
                 MailAddressToGroupModel.address_id == MailAddressModel.id). \
            join(cls, cls.id == MailAddressToGroupModel.group_id). \
            filter(MailAddressModel.address.in_(mail_addresses),
                   cls.id == group_id). \
            all()
        saved_addresses = {m.address for m in saved_address_models}
        not_tied_addresses = mail_addresses - saved_addresses

        # すでにDBに登録されているメアドを取得
        saved_address_models = session.query(MailAddressModel). \
            filter(MailAddressModel.address.in_(not_tied_addresses)). \
            all()
        session.add_all(
            [MailAddressToGroupModel(m.id, group_id)
             for m in saved_address_models]
        )

        saved_addresses = {m.address for m in saved_address_models}
        new_addresses = not_tied_addresses - saved_addresses
        mail_address_models = [
            MailAddressModel(address)
            for address in new_addresses
        ]
        session.add_all(mail_address_models)
        session.flush()

        mail_address_to_group_models = [
            MailAddressToGroupModel(address_model.id, group_id)
            for address_model in mail_address_models
        ]
        session.add_all(mail_address_to_group_models)

    @classmethod
    def delete(cls, id: int) -> None:

        session.query(MachineModel). \
            filter(MachineModel.group_id == id). \
            delete()

        session.query(MailAddressToGroupModel). \
            filter(MailAddressToGroupModel.group_id == id).\
            delete()

        session.query(cls). \
            filter(cls.id == id). \
            delete()
