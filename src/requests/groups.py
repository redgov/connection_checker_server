from pydantic import BaseModel


class GroupsPostIn(BaseModel):
    """グループ作成時のリクエストモデル
    """
    name: str
    mail_addresses_text: str


class GroupsPutIn(BaseModel):
    """グループ編集時のリクエストモデル
    """
    id: int
    name: str
    mail_addresses_text: str
