from datetime import date

from pydantic import BaseModel, EmailStr

from app.patients.models import CorrectGender


class SPatient(BaseModel):
    photo_url: str
    first_name: str
    last_name: str
    patronymic: str
    date_birthday: date
    number_passport: int
    series_passport: int
    gender: CorrectGender
    address: str
    phone_number: int
    email: EmailStr
