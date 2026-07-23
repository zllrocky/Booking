from uuid import UUID
from fastapi import HTTPException

from app.admin.schemas import SAdminUpdateStatus, SAdminUpdateIsActive
from app.users.dao import UsersDAO
from app.users.schemas import SUserRead, SUserWithBookings


async def update_status_for_id(user_id: UUID, admin_data: SAdminUpdateStatus) -> SUserRead:
    current_user = await UsersDAO.find_one_or_none(user_id=user_id)
    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')
    admin_dict = admin_data.model_dump(exclude_unset=True)
    update_user = await UsersDAO.update(filter_by={'id': user_id},
                                          data=admin_dict)
    return update_user


async def get_all_users_for_admin( limit: int = 50, offset: int = 0) -> list[SUserRead]:
    return await UsersDAO.find_all(limit=limit, offset=offset)


async def update_status_for_bool(user_id: UUID, admin_data: SAdminUpdateIsActive) -> SUserRead:
    current_user = await UsersDAO.find_one_or_none(user_id=user_id)
    if not current_user:
        raise HTTPException(status_code=404, detail='Not found')
    admin_dict = admin_data.model_dump(exclude_unset=True)
    update_user = await UsersDAO.update(filter_by={'id': user_id}, data=admin_dict)
    return update_user


async def get_all_info_for_users_and_bookings(user_id: UUID) -> SUserWithBookings:
    current_user = await UsersDAO.find_user_with_bookings(user_id=user_id)
    if not current_user:
        raise HTTPException(status_code=404, detail='Not found')
    return current_user