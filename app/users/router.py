from fastapi import APIRouter, Depends
from typing import Annotated

from app.auth.auth import get_current_active_user
from app.users.schemas import SUserRead
from app.users.models import Users
from app.users.services import register_user
from app.users.schemas import SUserAuth, SMessageForUserResponse


router = APIRouter(prefix='/user', tags=['User'])


@router.post('/register', status_code=201, response_model=SMessageForUserResponse,
             summary='New User Registration',
             description='Accepts an email address and password. Hashes the password and'
                         ' saves the user in the database. Returns a success message.'
                         ' If the email address already exists, returns a 409 Conflict error.')
async def create_user(user_data: SUserAuth):
    await register_user(user_data)
    return {
        "message": "The user has been successfully registered",
        'email': user_data.email
    }


@router.get("/me/", summary='Get User Info',
            description="Returns the current user's data (ID, email, activity status)."
                        " Available only to authorized users with a valid JWT token.")
async def read_users_me(
    current_user: Annotated[Users, Depends(get_current_active_user)],
) -> SUserRead:
    return SUserRead.model_validate(current_user)


