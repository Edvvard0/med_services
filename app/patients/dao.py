from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.patients.models import Patient


class PatientDAO(BaseDAO):
    model = Patient

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        new_instance = cls.model(**values)
        session.add(new_instance)

        try:
            await session.commit()
            await session.refresh(new_instance)
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance
