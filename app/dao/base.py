from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker


class BaseDAO:
    model = None


    @classmethod
    async def find_all(cls, **filter_by):
        clean_filters = {k: v for k, v in filter_by.items() if v is not None}
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**clean_filters)
            result = await session.execute(query)
            return result.scalars().all()


    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()


    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            try:
                query = insert(cls.model).values(**data).returning(cls.model)
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one_or_none()
            except SQLAlchemyError as e:
                print(f'Database error {e}')
                return None


    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount


    @classmethod
    async def update(cls, filter_by: dict, data: dict):
        async with async_session_maker() as session:
            query = update(cls.model).filter_by(**filter_by).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

