from fastapi import APIRouter, UploadFile, Depends, HTTPException

from pydantic import EmailStr
from starlette import status
from starlette.responses import FileResponse, StreamingResponse, Response

from app.database import SessionDep, get_session, async_session_maker
from app.exception import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.patients.auth import get_password_hash, authenticate_user, create_access_token
from app.patients.dao import PatientDAO
from app.patients.dependencies import get_current_user
from app.patients.schemas import SPatientAdd, SPatien, SPatientAuth
from app.patients.utils import recognize_qr_code, generate_qr_code, generate_consent, generate_contract

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@router.post("/")
async def add_patient(data_patient: SPatientAdd, session: SessionDep):
    user = await PatientDAO.find_one_or_none(session=session, email=data_patient.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )

    hashed_password = get_password_hash(data_patient.password)
    data_patient.password = hashed_password

    async with async_session_maker() as session:
        await PatientDAO.add(session, **data_patient.model_dump())
    return {"message": "Пользователь успешно добавлен"}


@router.get("/")
async def all_patients(session: SessionDep) -> list[SPatien]:
    patients = await PatientDAO.find_all(session)
    return patients


@router.post('/login')
async def login_user(response: Response, patient_data: SPatientAuth, session: SessionDep):
    patient = await authenticate_user(patient_data.email, patient_data.password, session)
    if not patient:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(patient.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return access_token


@router.get("/me")
async def get_me(patient=Depends(get_current_user)) -> SPatien:
    return patient


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


@router.get("/{patient_id}")
async def get_patient(patient_id: int, session: SessionDep) -> SPatien:
    patient = await PatientDAO.find_one_or_none_by_id(session=session, model_id=patient_id)
    return patient
