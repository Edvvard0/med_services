from datetime import date

from pydantic import BaseModel

from app.doctors.schemas import SDoctor
from app.patients.schemas import SPatient


class SHospitalization(BaseModel):
    patient_id: int
    doctor_id: int

    department: str
    purpose: str
    start_date: date
    end_date: date
    is_paid: bool

    refusal_patient: bool
    refusal_doctor: bool
    cancel_reason: str


class SHospitalizationFull(SHospitalization):
    patients: SPatient
    doctors: SDoctor
