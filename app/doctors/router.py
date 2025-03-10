from fastapi import APIRouter

from app.database import SessionDep
from app.doctors.dao import DoctorDAO
from app.doctors.schemas import SDoctor

router = APIRouter(
    prefix="/doctors",
    tags=["doctors"]
)


@router.get("/")
async def get_all_doctors(session: SessionDep) -> list[SDoctor]:
    doctors = await DoctorDAO.find_all(session)
    return doctors


@router.post("/")
async def add_doctors(session: SessionDep, doctor: SDoctor):
    await DoctorDAO.add(session, **doctor.model_dump())
    return {"message": "Доктор успешно зарегистрирован"}


@router.get("/{doctor_id}")
async def get_current_doctor(
        session: SessionDep,
        doctor_id: int
        ) -> SDoctor | None:
    doctor = await DoctorDAO.find_one_or_none_by_id(session, model_id=doctor_id)
    return doctor
