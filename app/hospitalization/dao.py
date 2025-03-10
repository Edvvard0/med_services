import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.hospitalization.models import Hospitalization


class HospitalizationDAO(BaseDAO):
    model = Hospitalization

    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession, hosp_id: uuid.UUID):
        query = select(cls.model).filter_by(id=hosp_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
