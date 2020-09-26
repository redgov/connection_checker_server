from fastapi import APIRouter

from src.constants import PATH, TAGS
from src.requests.groups import GroupsPostIn
from src.services.groups import GroupService


router = APIRouter()


@router.post(PATH.GROUPS,
             tags=[TAGS.GROUPS])
async def create_group(groups_post_in: GroupsPostIn):
    group_service = GroupService()
    group_service.create(groups_post_in.name,
                         groups_post_in.mail_addresses_text)
