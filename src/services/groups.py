from src.db_setting import Session
from src.models.group import GroupModel
from src.responses.groups import GroupsOut, GroupInfo
 

session = Session()


class GroupsService:

    def get(self) -> GroupsOut:
        """get groups info
        """
        groups = GroupModel.get()
        groups_out = GroupsOut(groups=[
            GroupInfo(id=g["id"], name=g["name"], to_addresses=g["addresses"])
            for g in groups
        ])

        return groups_out

    def create(self, name: str, mail_addresses_text: str):
        """create new group

        Parameters
        ----------
        name : str
            グループ名
        mail_addresses_text : str
            改行で区切られたメールアドレス群の文字列
        """

        mail_addresses = mail_addresses_text.splitlines()
        # 前後の空白削除
        mail_addresses = {address.strip() for address in mail_addresses}
        mail_addresses = {a for a in mail_addresses if a == ""}
        GroupModel.save(name, mail_addresses)
        session.commit()

    def delete(self, id: int):
        """delete selected group

        Parameters
        ----------
        id : int
            削除対象のグループのid
        """
        GroupModel.delete(id)
        session.commit()
