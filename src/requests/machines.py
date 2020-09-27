from pydantic import BaseModel


class MachinesPostIn(BaseModel):
    """マシン追加時のリクエストモデル
    """
    group_id: int
    name: str
    ip_address: str
