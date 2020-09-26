from pydantic import BaseModel


class GroupsPostIn(BaseModel):
    """グループ作成時のリクエストモデル
    """
    name: str
    mail_addresses_text: str
