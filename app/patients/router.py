from fastapi import APIRouter, UploadFile
from starlette.responses import FileResponse, StreamingResponse

from app.database import SessionDep
from app.patients.dao import PatientDAO
from app.patients.schemas import SPatientAdd, SMedCardAdd
from app.patients.utils import recognize_qr_code, generate_qr_code, generate_consent, generate_contract

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@router.get("/{patient_id}")
async def get_patient(patient_id: int, session: SessionDep) -> SPatientAdd:
    patient = await PatientDAO.find_one_or_none_by_id(session=session, model_id=patient_id)
    print(patient)
    return patient


@router.post("/")
async def add_patient(data_patient: SPatientAdd, session: SessionDep):
    await PatientDAO.add(session, **data_patient.model_dump())
    return {"message": "Пользователь успешно добавлен"}


@router.post("/upload_photo")
async def upload_photo(uploaded_file: UploadFile):
    '''  Добавить сохранение в s3 хранилище'''
    # file = uploaded_file.file
    # file_name = "data/photo.jpg"
    # with open(file_name, "wb") as f:
    #     f.write(file.read())


@router.get("/qr_code/{patient_id}")
async def get_qr_code_patient(patient_id: int):
    qr_buffer = await generate_qr_code(str(patient_id))
    return StreamingResponse(qr_buffer, media_type="image/jpeg")


@router.post("/qr_code")
async def recognition_qr_code_patient(uploaded_file: UploadFile):
    file_content = await uploaded_file.read()
    data = await recognize_qr_code(file_content)
    return {"data": data}


@router.get("/consent/{patient_id}")
async def consent(patient_id: int, session: SessionDep):
    patient = await PatientDAO.find_one_or_none_by_id(session, model_id=patient_id)
    file_path = await generate_consent(patient)

    return FileResponse(
        path=file_path,
        filename="Согласие_на_обработку_данных.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@router.get("/contract/{patient_id}")
async def contract(patient_id: int, session: SessionDep):
    patient = await PatientDAO.find_one_or_none_by_id(session, model_id=patient_id)

    file_path = await generate_contract(patient)

    return FileResponse(
        path=file_path,
        filename="Договор.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )