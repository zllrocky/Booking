from sqlalchemy import ForeignKey, Numeric
from decimal import Decimal
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID
from typing import TYPE_CHECKING

from app.database import Base

if TYPE_CHECKING:
    from app.booking.models import Bookings
    from app.hotels.models import Hotels



class Rooms(Base):
    __tablename__ = 'rooms'

    room_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.hotel_id', ondelete='CASCADE'))
    name: Mapped[str]
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    quantity: Mapped[int]
    facilities: Mapped[list[str]] = mapped_column(JSONB, nullable=True)

    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")
    bookings: Mapped[list["Bookings"]] = relationship(back_populates="room")