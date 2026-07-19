from typing import Annotated
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
import jwt

from app.users.models import Role
from app.auth.auth import oauth2_scheme
from app.config import settings
from app.users.models import Users
from app.users.dao import UsersDAO
from app.auth.schemas import STokenData


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = STokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = await UsersDAO.find_one_or_none(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[Users, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class RoleChecker:
    def __init__(self, allowed_roles: list[Role]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: Users = Depends(get_current_active_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException (status_code=403, detail='Not enough permissions')
        return current_user


DependsActiveUser = Annotated[Users, Depends(get_current_active_user)]
DependsAdminOrOwner = Annotated[Users, Depends(RoleChecker([Role.ADMIN, Role.OWNER]))]
DependsAdminOrUser = Annotated[Users, Depends(RoleChecker([Role.ADMIN, Role.USER]))]