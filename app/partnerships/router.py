from fastapi import APIRouter

from app.dependencies import DependsActiveUser
from app.partnerships.schemas import SPartnershipsRequestCreate, \
    SPartnershipsRequestResponse
from app.partnerships.services import create_partnership_request, \
    check_status_partnership

router = APIRouter(prefix='/partnerships', tags=['Partnerships'])


@router.post('/request', summary='Add a Partnership Application', description='')
async def create_partnership(partnership_data: SPartnershipsRequestCreate,
                             user: DependsActiveUser) -> SPartnershipsRequestResponse:
    return await create_partnership_request(partnership_data=partnership_data, user_id=user.id)


@router.get('/me', summary='My Requests', description='')
async def check_status(user: DependsActiveUser) -> list[SPartnershipsRequestResponse]:
    return await check_status_partnership(user_id=user.id)