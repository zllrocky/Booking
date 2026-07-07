from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class SUserAuth(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8,
                                   max_length=72,
                                   description='A password of between 8 and 72 characters')]


class SMessageForUserResponse(BaseModel):
    message: str
    email: EmailStr


