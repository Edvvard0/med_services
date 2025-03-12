import uuid

from fastapi import APIRouter
from sqlalchemy.orm import selectinload

from app.database import SessionDep
from app.hospitalization.dao import HospitalizationDAO
from app.hospitalization.models import Hospitalization
from app.hospitalization.schemas import SHospitalization

router = APIRouter(
    prefix="/hospitalizations",
    tags=["hospitalizations"]
)


@router.get("/")
async def get_hospitalizations(session: SessionDep) -> list[SHospitalization]:
    hosp = await HospitalizationDAO.find_all(session)
    return hosp


@router.post("/")
async def add_hospitalization(session: SessionDep, hosp: SHospitalization):
    await HospitalizationDAO.add(session, **hosp.model_dump())
    return {"message": "Госпитализация успешно добавлена"}


@router.get("/patients/{hosp_id}")
async def get_patients_hosp(session: SessionDep, hosp_id: str):
    hosp_id = uuid.UUID(hosp_id)
    rez = await HospitalizationDAO.find_patient_by_hosp_id(session=session,
                                                           hosp_id=hosp_id,
                                                           options=[selectinload(Hospitalization.patients)])
    return rez


@router.get("/{hosp_id}")
async def get_current_hosp(hosp_id: str, session: SessionDep) -> SHospitalization | None:
    hosp_id = uuid.UUID(hosp_id)
    hosp = await HospitalizationDAO.find_one_or_none_by_id(session, hosp_id=hosp_id)
    return hosp


