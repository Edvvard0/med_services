from fastapi import APIRouter
from sqlalchemy.orm import selectinload

from app.database import SessionDep
from app.med_procedure.dao import MedProcedureDAO
from app.med_procedure.models import MedProcedure

router = APIRouter(
    prefix="/med_procedure",
    tags=["med_procedure"]
)


@router.get("/")
async def get_all_med_procedure(session: SessionDep):
    rez = await MedProcedureDAO.find_all_med_procedures(
        session,
        options=[selectinload(MedProcedure.patients),
                 selectinload(MedProcedure.doctors),
                 selectinload(MedProcedure.cabinet)])
    return rez


@router.get("/{med_procedures_id}")
async def get_med_procedures(session: SessionDep, med_procedures_id: int):
    rez = await MedProcedureDAO.find_med_procedures(
        session,
        med_procedures_id,
        options=[selectinload(MedProcedure.patients),
                 selectinload(MedProcedure.doctors),
                 selectinload(MedProcedure.cabinet)])
    return rez
