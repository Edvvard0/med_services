from fastapi import APIRouter, UploadFile

from pydantic import EmailStr
from starlette.responses import FileResponse, StreamingResponse, Response

from app.database import SessionDep
from app.exception import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.patients.auth import get_password_hash, authenticate_user, create_access_token
from app.patients.dao import PatientDAO
from app.patients.schemas import SPatientAdd, SPatien, SPatientAuth
from app.patients.utils import recognize_qr_code, generate_qr_code, generate_consent, generate_contract

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@router.get("/{patient_id}")
async def get_patient(patient_id: int, session: SessionDep) -> SPatien:
    patient = await PatientDAO.find_one_or_none_by_id(session=session, model_id=patient_id)
    return patient


@router.post("/")
async def add_patient(data_patient: SPatientAdd, session: SessionDep):
    # existing_patient = await PatientDAO.find_one_or_none(session, email=data_patient.email)
    # if existing_patient:
    #     raise UserAlreadyExistsException

    hashed_password = get_password_hash(data_patient.password)
    data_patient.password = hashed_password

    await PatientDAO.add(session, **data_patient.model_dump())
    return {"message": "Пользователь успешно добавлен"}


@router.post('/login')
async def login_user(response: Response, user_data: SPatientAuth, session: SessionDep):
    user = await authenticate_user(user_data.email, user_data.password, session)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return access_token


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


# @router.post('/register')
# async def register_user(user_data: SUserAuth):
#     existing_user = await UserDAO.find_one_or_none(email=user_data.email)
#     if existing_user:
#         raise UserAlreadyExistsException
#     hashed_password = get_password_hash(user_data.password)
#     await UserDAO.add(email=user_data.email, hashed_password=hashed_password)
#
#
# @router.post('/login')
# async def login_user(response: Response, user_data: SUserAuth):
#     user = await authenticate_user(user_data.email, user_data.password)
#     if not user:
#         raise IncorrectEmailOrPasswordException
#     access_token = create_access_token({'sub': str(user.id)})
#     response.set_cookie("booking_access_token", access_token, httponly=True)
#     return access_token
