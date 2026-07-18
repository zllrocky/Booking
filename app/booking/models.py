from uuid import UUID, uuid4
from datetime import date
import enum
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BookingStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Bookings(Base):
    __tablename__ = 'bookings'

    booking_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    room_id: Mapped[UUID] = mapped_column(ForeignKey('rooms.room_id'))
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[Decimal]
    total_cost: Mapped[Decimal]
    total_days: Mapped[int]
    status: Mapped[BookingStatus] = mapped_column(default=BookingStatus.PENDING)