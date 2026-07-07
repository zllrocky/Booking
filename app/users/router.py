from fastapi import APIRouter

from app.users.services import register_user
from app.users.schemas import SUserAuth, SMessageForUserResponse


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register', status_code=201, response_model=SMessageForUserResponse)
async def create_user(user_data: SUserAuth):
    await register_user(user_data)
    return {
        "message": "The user has been successfully registered",
        'email': user_data.email
    }



@router.get('')
async def get_user():
    pass