import uuid
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.patients.models import CorrectGender


class SPatientAdd(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    date_birthday: date
    passport: str
    gender: CorrectGender
    address: str
    phone_number: str
    email: EmailStr

    photo_url: str
    date_issue: date
    date_last_request: datetime
    date_next_visit: datetime
    number_insurance_policy: str
    date_expiration: date
    diagnosis: str
    disease_history: str

    insurance_company: str
    password: str


class SPatient(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str
    date_birthday: date
    gender: CorrectGender
    address: str
    phone_number: str
    email: EmailStr

    date_issue: date
    date_last_request: datetime
    date_next_visit: datetime
    number_insurance_policy: str
    date_expiration: date
    diagnosis: str
    disease_history: str

    insurance_company: str


class SPatientAuth(BaseModel):
    email: EmailStr
    password: str
