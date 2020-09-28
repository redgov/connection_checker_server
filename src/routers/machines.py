from fastapi import APIRouter

from src.constants import PATH, TAGS
from src.requests.machines import MachinesPostIn
from src.responses.machines import MachinesOut
from src.services.machines import MachinesService


router = APIRouter()


@router.get(PATH.MACHINES,
            response_model=MachinesOut,
            tags=[TAGS.MACHINES])
async def get_machines():
    machines_service = MachinesService()
    machine_out = machines_service.get()
    return machine_out


@router.post(PATH.MACHINES,
             tags=[TAGS.MACHINES])
async def create_group(machines_post_in: MachinesPostIn):
    machines_service = MachinesService()
    machines_service.create(
        machines_post_in.group_id,
        machines_post_in.name,
        machines_post_in.ip_address,
    )
