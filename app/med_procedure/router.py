from fastapi import APIRouter, Depends
from sqlalchemy.orm import selectinload

from app.database import SessionDep
from app.doctors.dependencies import get_current_user
from app.med_procedure.dao import MedProcedureDAO, CabinetDAO
from app.med_procedure.models import MedProcedure
from app.med_procedure.schemas import SCabinet, SMedProcedureAdd, SMedProcedureFull

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


@router.get("/patient/{patient_id}")
async def get_all_med_procedure_by_current_patient(session: SessionDep, patient_id: int) -> list[SMedProcedureFull]:
    rez = await MedProcedureDAO.find_all_med_procedures_current_patient(
        session,
        patient_id=patient_id,
        options=[selectinload(MedProcedure.patients),
                 selectinload(MedProcedure.doctors),
                 selectinload(MedProcedure.cabinet)])
    return rez


@router.post("/patient/{patient_id}")
async def add_med_procedure(
        session: SessionDep,
        patient_id: int,
        med_procedure_data: SMedProcedureAdd,
        doctor=Depends(get_current_user)):
    data = med_procedure_data.model_dump()
    data["patient_id"] = patient_id
    data["doctor_id"] = doctor.id
    data["type_procedure"] = med_procedure_data.type_procedure.value

    await MedProcedureDAO.add(session, **data)
    return {"message": "МедПроцедура успешно добавлена"}


@router.get("/cabinets")
async def get_all_cabinets(session: SessionDep) -> list[SCabinet]:
    cabinets = await CabinetDAO.find_all(session)
    return cabinets


@router.get("/{med_procedures_id}")
async def get_med_procedures(session: SessionDep, med_procedures_id: int):
    rez = await MedProcedureDAO.find_med_procedures(
        session,
        med_procedures_id,
        options=[selectinload(MedProcedure.patients),
                 selectinload(MedProcedure.doctors),
                 selectinload(MedProcedure.cabinet)])
    return rez
