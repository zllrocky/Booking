import enum
import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.users.models import Users


class RequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class PartnershipsRequests(Base):
    __tablename__ = "partnership_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    company_name: Mapped[str] = mapped_column(String)
    tax_id: Mapped[str] = mapped_column(String)
    contact_phone: Mapped[str] = mapped_column(String)
    contact_email: Mapped[str] = mapped_column(String)
    status: Mapped[RequestStatus] = mapped_column(default=RequestStatus.PENDING)
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=lambda: datetime.datetime.now(datetime.UTC).replace(tzinfo=None))

    user: Mapped["Users"] = relationship(back_populates="partnership_requests")
