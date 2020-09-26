from typing import List, Optional
from pydantic import BaseModel


class GroupInfo(BaseModel):
    id: int
    name: str
    to_addresses: List[str]


class GroupsOut(BaseModel):
    groups: List[GroupInfo]

    class Config:
        schema_extra = {
            "example": [{
                "id": 1,
                "name": "Foo",
                "to_addresses": ["google@yahoo.co.jp", "amazon@gmail.com"]
            },{
                "id": 2,
                "name": "Faa",
                "to_addresses": ["google@yahoo.co.jp", "amazon@gmail.com"]
            },
            ]
        }