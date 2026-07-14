from sqlalchemy import ForeignKey, Numeric
from decimal import Decimal
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4, UUID

from app.database import Base


class Rooms(Base):
    __tablename__ = 'rooms'

    room_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.hotel_id'))
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    facilities: Mapped[list[str]] = mapped_column(JSONB, nullable=True)