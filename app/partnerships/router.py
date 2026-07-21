from fastapi import APIRouter

from app.partnerships.models import RequestStatus
from app.dependencies import DependsActiveUser, DependsAdmin
from app.partnerships.schemas import SPartnershipsRequestCreate, \
    SPartnershipsRequestResponse, SPartnershipsUpdate
from app.partnerships.services import create_partnership_request, \
    check_status_partnership, get_all_status_partnership, update_status_partnership, \
    get_partnership_for_id, delete_partnership_status

router = APIRouter(prefix='/partnerships', tags=['Partnerships'])


@router.post('/request', summary='[AUTH] Add a Partnership Application',
             description="**Access**: Authorized users only.\nCreates a new request."
                         " The system automatically retrieves the `user_id` from the "
                         "authorization token and sets the request's initial status.")
async def create_partnership(partnership_data: SPartnershipsRequestCreate,
                             user: DependsActiveUser) -> SPartnershipsRequestResponse:
    return await create_partnership_request(partnership_data=partnership_data, user_id=user.id)


@router.get('/me', summary='[AUTH] Get my Requests',
            description='**Access**: Authorized users only.\nReturns a list of all '
                        'partnership requests created by the current user.')
async def check_status(user: DependsActiveUser) -> list[SPartnershipsRequestResponse]:
    return await check_status_partnership(user_id=user.id)


@router.get('/all', summary='[ADMIN] Get all applications',
            description='**Access**: Administrators only.\nReturns a complete list of'
                        ' requests in the system. Supports optional filtering via the'
                        ' `status` query parameter (for example, `status=pending`).')
async def get_all_partnerships(_: DependsAdmin, status: RequestStatus | None = None
                               ) -> list[SPartnershipsRequestResponse]:
    return await get_all_status_partnership(status=status)


@router.get('/{partnership_id}', summary='[ADMIN] Get a request by ID',
            description='**Access**: Administrators only.\nReturns detailed information '
                        'about a specific request based on its unique identifier.')
async def get_partnership_id(partnership_id: int, _ : DependsAdmin
                                 ) -> SPartnershipsRequestResponse:
    return await get_partnership_for_id(partnership_id=partnership_id)



@router.patch('/{partnership_id}', summary='[ADMIN] Update Application Status',
              description='**Access**: Administrators only.\nChanges the current status of'
                          ' a request (for example, to `approved` or `rejected`)'
                          ' and returns the updated data.')
async def update_status(partnership_id: int, partnership_data: SPartnershipsUpdate,
                        _ : DependsAdmin) -> SPartnershipsRequestResponse:
    return await update_status_partnership(partnership_id=partnership_id,
                                           status=partnership_data.status)


@router.delete('/{partnership_id}', status_code=204,
               summary='[ADMIN] Delete request',
               description='**Access**: Administrators only.\nCompletely deletes the '
                           'request from the database without the possibility of recovery.'
                           ' If successful, returns an empty response `204 No Content`.')
async def delete_partnership(partnership_id: int, _ : DependsAdmin) -> None:
    return await delete_partnership_status(partnership_id=partnership_id)