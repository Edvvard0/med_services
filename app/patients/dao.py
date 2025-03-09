from app.dao.base import BaseDAO
from app.patients.models import Patient, MedCard


class PatientDAO(BaseDAO):
    model = Patient


class MedCardDAO(BaseDAO):
    model = MedCard
