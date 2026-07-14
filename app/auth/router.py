
from fastapi import APIRouter
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.schemas import SToken
from app.auth.auth import authenticate_user, create_access_token
from app.config import settings


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/login", summary="User Authentication",
             description="Accepts an email address and password, and returns a JWT token")
async def login_for_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> SToken:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return SToken(access_token=access_token, token_type="bearer")


