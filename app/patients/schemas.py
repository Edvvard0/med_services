from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.patients.models import CorrectGender


class SMedCardAdd(BaseModel):
    patient_id: int
    photo_url: str
    date_issue: date
    date_last_request: datetime
    date_next_visit: datetime
    number_insurance_policy: str
    date_expiration: date
    diagnosis: str
    disease_history: str


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
    insurance_company: str
