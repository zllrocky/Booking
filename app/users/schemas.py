from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.booking.schemas import SBooking
from app.users.models import Role


OptionalPassword = Annotated[str | None, Field(default=None,
                                 min_length=8,
                                 max_length=72,
                                 description='A password of between 8 and 72 characters')]


class SUserAuth(BaseModel):
    email: EmailStr
    password: OptionalPassword


class SUserRead(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    status: Role

    model_config = ConfigDict(from_attributes=True)


class SUserUpdate(BaseModel):
    email: EmailStr | None = None
    old_password: OptionalPassword
    password: OptionalPassword


class SUserWithBookings(SUserRead):
    bookings: list[SBooking]
