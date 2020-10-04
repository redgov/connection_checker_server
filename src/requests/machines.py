from pydantic import BaseModel


class MachinesPostIn(BaseModel):
    """マシン追加時のリクエストモデル
    """
    group_id: int
    name: str
    ip_address: str


class MachinesPutIn(BaseModel):
    """マシン編集時のリクエストモデル
    """
    machine_id: int
    group_id: int
    name: str
    ip_address: str
    is_active: bool
