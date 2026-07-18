from uuid import UUID
from datetime import date
from sqlalchemy import select, and_

from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.booking.models import Bookings


class BookingDAO(BaseDAO):
    model = Bookings


    @classmethod
    async def check_overbooking(cls, room_id: UUID, date_from: date, date_to: date,
                                booking_id: UUID | None = None):
        query = select(cls.model).where(
            and_(
                cls.model.room_id == room_id,
                cls.model.date_from < date_to,
                cls.model.date_to > date_from
            )
        )
        if booking_id is not None:
            query = query.where(cls.model.booking_id != booking_id)

        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.scalars().first()