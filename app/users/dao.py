from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def find_user_with_bookings(cls, user_id: UUID):
        async with async_session_maker() as session:
            query = select(Users).where(Users.id == user_id).options(
                selectinload(Users.bookings))
            result = await session.execute(query)
            return result.scalar_one_or_none()