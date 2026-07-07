from fastapi import HTTPException

from app.users.auth import get_password_hash
from app.users.dao import UsersDAO
from app.users.schemas import SUserAuth


async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=409, detail='The user already exists')
    hashed_password = get_password_hash(user_data.password)
    new_user = await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    if not new_user:
        raise HTTPException(status_code=500, detail='Internal Server Error')
