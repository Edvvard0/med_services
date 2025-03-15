from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class TypeProcedure(Enum):
    LAB_RESEARCH = "лабораторное исследование"
    DIAGNOSTICS = "инструментальная диагностика"
    DRUG_TERAPY = "лекарственная терапия"
    PHYSICAL_THERAPY = "физиотерапия"
    SURGICAL_TREATMENT = "хирургическое лечение"


class SMedProcedure(BaseModel):
    patient_id: int
    doctor_id: int
    cabinet_id: int

    datetime_measures: datetime
    type_procedure: TypeProcedure
    name_measures: str
    result: str
    recommendations: str


class SMedProcedureAdd(BaseModel):
    cabinet_id: int

    datetime_measures: datetime
    type_procedure: TypeProcedure
    name_measures: str
    result: str
    recommendations: str


class SCabinet(BaseModel):
    id: int
    number_cabinet: int
    name: str
