from src.db_setting import Session
from src.models.group import GroupModel


session = Session()

class GroupService:

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
        mail_addresses = [address.strip() for address in mail_addresses]
        GroupModel.save(name, mail_addresses)
        session.commit()
