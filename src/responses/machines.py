from typing import List, Optional
from pydantic import BaseModel


class MachineInfo(BaseModel):
    id: int
    name: str
    ip_address: str
    is_success_last: Optional[bool]
    success_time: Optional[str]
    failure_time: Optional[str]
    is_active: bool
    group_id: int

    class Config:
        orm_mode = True


class MachinesOut(BaseModel):
    machines: List[MachineInfo]

    class Config:
        orm_mode = True
