from fastapi import APIRouter
from sqlalchemy.orm import selectinload

from app.database import SessionDep
from app.med_procedure.dao import MedProcedureDAO
from app.med_procedure.models import MedProcedure

router = APIRouter(
    prefix="/med_procedure",
    tags=["med_procedure"]
)


@router.get("/{med_procedures}")
async def get_med_procedures(session: SessionDep, med_procedures: int):
    rez = await MedProcedureDAO.find_med_procedures(
        session,
        med_procedures,
        options=[selectinload(MedProcedure.patients),
                 selectinload(MedProcedure.doctors),
                 selectinload(MedProcedure.cabinet)])
    return rez
