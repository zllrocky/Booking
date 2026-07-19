from fastapi import APIRouter

from app.users.schemas import SUserRead, SUserUpdate
from app.users.services import register_user, update_user, delete_user
from app.users.schemas import SUserAuth
from app.dependencies import DependsActiveUser


router = APIRouter(prefix='/user', tags=['Users'])


@router.post('/register', status_code=201,
             summary='Create User',
             description='Accepts an email address and password. Hashes the password and'
                         ' saves the user in the database.<br> Returns a success message.<br>'
                         ' If the email address already exists, returns a 409 Conflict error.')
async def create_user(user_data: SUserAuth):
    return await register_user(user_data)


@router.get("/me/", summary='Get User Info',
            description="Returns the current user's data (ID, email, activity status).<br>"
                        " Available only to authorized users with a valid JWT token.")
async def read_users_me(current_user: DependsActiveUser):
    return SUserRead.model_validate(current_user)


@router.patch("/me", summary='Update Profile Information',
              description='Partial update of the currently logged-in users data.<br>'
                          'You can submit only the email address, only the password, or both fields at once<br>'
                          'If you submit a password, it must contain between 8 and 72 characters.<br>'
                          'To change your password, you must provide your current password (old_password) for verification.')
async def update_user_profile(
    user_data: SUserUpdate,
    current_user: DependsActiveUser
):
    return await update_user(user_id=current_user.id, user_data=user_data)


@router.delete('/me',status_code=204, summary='Delete a users profile',
               description='Completely and permanently delete the currently logged-in'
                           ' users account from the database.<br> The user is automatically'
                           ' identified by the JWT token stored in cookies.<br>'
                           ' Warning: This action cannot be undone.')
async def delete_user_profile(current_user: DependsActiveUser):
    await delete_user(user_id=current_user.id)




