from fastapi import APIRouter

from src.constants import PATH, TAGS
from src.requests.groups import GroupsPostIn, GroupsPutIn
from src.responses.groups import GroupsOut
from src.services.groups import GroupsService


router = APIRouter()


@router.get(PATH.GROUPS,
            response_model=GroupsOut,
            tags=[TAGS.GROUPS])
async def get_groups_info():
    group_service = GroupsService()
    groups = group_service.get()
    return groups


@router.post(PATH.GROUPS,
             tags=[TAGS.GROUPS])
async def create_group(groups_post_in: GroupsPostIn):
    group_service = GroupsService()
    group_service.create(
        groups_post_in.name,
        groups_post_in.mail_addresses_text
    )


@router.put(PATH.GROUPS,
            tags=[TAGS.GROUPS])
async def edit_group(groups_put_in: GroupsPutIn):
    group_service = GroupsService()
    group_service.update(
        groups_put_in.id,
        groups_put_in.name,
        groups_put_in.mail_addresses_text
    )


@router.delete(PATH.GROUPS,
               tags=[TAGS.GROUPS])
async def delete_group(id: int):
    group_service = GroupsService()
    group_service.delete(id)
