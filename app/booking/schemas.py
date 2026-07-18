from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel
from datetime import date

from app.booking.models import BookingStatus


class SBooking(BaseModel):
    booking_id: UUID
    room_id: UUID
    user_id: UUID
    date_from: date
    date_to: date
    price: Decimal
    total_cost: Decimal
    total_days:int
    status: BookingStatus

class SAddBooking(BaseModel):
    room_id: UUID
    date_from: date
    date_to: date


class SUpdateBooking(BaseModel):
    date_from: date
    date_to: date
