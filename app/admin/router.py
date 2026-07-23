from fastapi import APIRouter
from uuid import UUID

from app.admin.services import update_status_for_id, get_all_users_for_admin, \
    update_status_for_bool, get_all_info_for_users_and_bookings
from app.dependencies import DependsAdmin
from app.admin.schemas import SAdminUpdateStatus, SAdminUpdateIsActive
from app.users.schemas import SUserRead, SUserWithBookings

router = APIRouter(prefix='/admin', tags=['Admins'])


@router.patch('/users/{user_id}/role', summary='[ADMIN] Change a users role',
              description='')
async def update_status_role(user_id: UUID,
                             admin_data: SAdminUpdateStatus,
                             _ : DependsAdmin) -> SUserRead:
    return await update_status_for_id(user_id=user_id, admin_data=admin_data)


@router.get('/users', summary='[ADMIN] Get a list of all users')
async def get_all_users(_ : DependsAdmin,
                        limit: int = 50,
                        offset: int = 0) -> list[SUserRead]:
    return await get_all_users_for_admin(limit=limit, offset=offset)


@router.patch('/users/{user_id}/status', summary='[ADMIN]',
              description='')
async def update_status_bool(user_id: UUID,
                             admin_data: SAdminUpdateIsActive,
                             _ : DependsAdmin) -> SUserRead:
    return await update_status_for_bool(user_id=user_id, admin_data=admin_data)


@router.get('/users/{user_id}', summary='[ADMIN]', description='')
async def get_all_info_for_users(user_id: UUID,
                                              _ : DependsAdmin) -> SUserWithBookings:
    return await get_all_info_for_users_and_bookings(user_id=user_id)