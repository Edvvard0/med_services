from datetime import date

from pydantic import BaseModel


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
