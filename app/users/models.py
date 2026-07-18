from uuid import uuid4, UUID
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.database import Base


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