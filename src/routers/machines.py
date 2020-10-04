from fastapi import APIRouter

from src.constants import PATH, TAGS
from src.requests.machines import MachinesPostIn, MachinesPutIn
from src.responses.machines import MachinesOut
from src.services.machines import MachinesService


router = APIRouter()


@router.get(PATH.MACHINES,
            response_model=MachinesOut,
            tags=[TAGS.MACHINES])
async def get():
    machines_service = MachinesService()
    machine_out = machines_service.get()
    return machine_out


@router.post(PATH.MACHINES,
             tags=[TAGS.MACHINES])
async def create(machines_post_in: MachinesPostIn):
    machines_service = MachinesService()
    machines_service.create(
        machines_post_in.group_id,
        machines_post_in.name,
        machines_post_in.ip_address,
    )


@router.put(PATH.MACHINES,
             tags=[TAGS.MACHINES])
async def edit(machines_put_in: MachinesPutIn):
    machines_service = MachinesService()
    machines_service.edit(
        machines_put_in.machine_id,
        machines_put_in.group_id,
        machines_put_in.name,
        machines_put_in.ip_address,
        machines_put_in.is_active,
    )



@router.delete(PATH.MACHINES,
             tags=[TAGS.MACHINES])
async def delete(id: int):
    machines_service = MachinesService()
    machines_service.delete(id)
