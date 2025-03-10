from datetime import datetime

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MedProcedure(Base):
    __tablename__ = "med_procedures"

    patient_id: Mapped[int] = mapped_column(Integer,  ForeignKey("patients.id"))
    doctor_id: Mapped[int] = mapped_column(Integer,  ForeignKey("doctors.id"))
    cabinet_id: Mapped[int] = mapped_column(Integer,  ForeignKey("cabinets.id"))

    datetime_measures: Mapped[datetime]
    type_procedure: Mapped[str]
    name_measures: Mapped[str]
    result: Mapped[str]
    recommendations: Mapped[str]


class Cabinet(Base):
    number_cabinet: Mapped[int]
    name: Mapped[int]



