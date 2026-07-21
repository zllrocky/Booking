from fastapi import APIRouter

from app.users.schemas import SUserRead, SUserUpdate
from app.users.services import register_user, update_user, delete_user
from app.users.schemas import SUserAuth
from app.dependencies import DependsActiveUser


router = APIRouter(prefix='/user', tags=['Users'])


@router.post('/register', status_code=201,
             summary='[PUBLIC] Create User',
             description='**Access:** Public (no authorization required).\n'
                         'Hashes the password and saves the user in the database. '
                         'Returns a success message. If the email address already '
                         'exists, returns a 409 Conflict error.')
async def create_user(user_data: SUserAuth):
    return await register_user(user_data)


@router.get("/me/", summary='[AUTH] Get User Info',
            description="**Access:** Authorized users only.\n"
                        "Returns the current user's data (ID, email, activity status).")
async def read_users_me(current_user: DependsActiveUser):
    return SUserRead.model_validate(current_user)


@router.patch("/me", summary='[AUTH] Update Profile Information',
              description="**Access:** Authorized users only.\n"
                          "Partial update of the currently logged-in user's data. "
                          "To change the password, the current password (`old_password`) "
                          "must be provided for verification.")
async def update_user_profile(
    user_data: SUserUpdate,
    current_user: DependsActiveUser
):
    return await update_user(user_id=current_user.id, user_data=user_data)


@router.delete('/me',status_code=204, summary='[AUTH] Delete a users profile',
               description='**Access:** Authorized users only.\n'
                           'Completely and permanently deletes the currently logged-in '
                           'users account from the database. The user is automatically '
                           'identified by the JWT token.\n'
                           '**Warning:** This action cannot be undone.')
async def delete_user_profile(current_user: DependsActiveUser):
    await delete_user(user_id=current_user.id)




