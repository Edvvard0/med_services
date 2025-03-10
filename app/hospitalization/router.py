import uuid

from fastapi import APIRouter

from app.database import SessionDep
from app.hospitalization.dao import HospitalizationDAO
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


@router.get("/{hosp_id}")
async def get_current_hosp(hosp_id: uuid.UUID, session: SessionDep) -> SHospitalization | None:
    hosp = await HospitalizationDAO.find_one_or_none_by_id(session, hosp_id=hosp_id)
    return hosp
