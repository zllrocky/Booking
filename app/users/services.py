from uuid import UUID

from fastapi import HTTPException

from app.auth.auth import get_password_hash, verify_password
from app.users.dao import UsersDAO
from app.users.schemas import SUserAuth, SUserUpdate


async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=409, detail='The user already exists')
    hashed_password = get_password_hash(user_data.password)
    new_user = await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    if not new_user:
        raise HTTPException(status_code=500, detail='Internal Server Error')


async def login_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if not existing_user:
        raise HTTPException(status_code=404, detail='User not found')


async def update_user(user_id: UUID, user_data: SUserUpdate):
    current_user = await UsersDAO.find_one_or_none(id=user_id)
    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    data_to_update = {}
    if user_data.email:

        existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
        if existing_user and existing_user.id != user_id:

            raise HTTPException(status_code=409, detail='This email is already taken')
        data_to_update['email'] = user_data.email
    if user_data.password:

        if not user_data.old_password:
            raise HTTPException(status_code=400, detail='Old password is required')

        if not verify_password(user_data.old_password, current_user.hashed_password):
            raise HTTPException(status_code=400, detail='Invalid old password')

        data_to_update['hashed_password'] = get_password_hash(user_data.password)

    if data_to_update:
        await UsersDAO.update(filter_by={'id': user_id}, data=data_to_update)


async def delete_user(user_id: UUID):
    await UsersDAO.delete(id=user_id)