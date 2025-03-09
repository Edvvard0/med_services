from fastapi import APIRouter, UploadFile
from starlette.responses import FileResponse, StreamingResponse

from app.database import SessionDep
from app.patients.dao import PatientDAO
from app.patients.schemas import SPatient
from app.patients.utils import recognize_qr_code, generate_qr_code

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@router.get("/{patient_id}")
async def get_patient(patient_id: int, session: SessionDep) -> SPatient:
    patient = PatientDAO.find_one_or_none_by_id(session=session, model_id=patient_id)
    return patient


@router.post("/")
async def add_patient(data_patient: SPatient, session: SessionDep):
    await PatientDAO.add(session, **data_patient.model_dump())
    return {"message": "Пользователь успешно добавлен"}


@router.get("/qr_code/{patient_id}")
async def get_qr_code_patient(patient_id: int):
    qr_buffer = await generate_qr_code(str(patient_id))
    return StreamingResponse(qr_buffer, media_type="image/jpeg")


@router.post("/qr_code/")
async def recognition_qr_code_patient(uploaded_file: UploadFile):
    file_content = await uploaded_file.read()
    data = await recognize_qr_code(file_content)
    return {"data": data}
