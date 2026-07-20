from uuid import uuid4, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from typing import TYPE_CHECKING

from app.database import Base

if TYPE_CHECKING:
    from app.partnerships.models import PartnershipsRequests
    from app.booking.models import Bookings


class Role(enum.Enum):
    USER = "user"
    OWNER = "owner"
    ADMIN = "admin"


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[Role] = mapped_column(default=Role.USER)

    partnership_requests: Mapped[list["PartnershipsRequests"]] = relationship(
        back_populates="user")
    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")