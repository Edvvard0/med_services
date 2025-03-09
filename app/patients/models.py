import uuid
from datetime import date, datetime
from enum import Enum

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM as PgEnum, types

from app.database import Base


class CorrectGender(Enum):
    MAN: str = "man"
    WOMAN: str = "woman"


class Patient(Base):
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str] = mapped_column(nullable=False)
    date_birthday: Mapped[date] = mapped_column(nullable=False)

    passport: Mapped[str] = mapped_column(nullable=False)

    gender: Mapped[str] = mapped_column(PgEnum(CorrectGender,
                                               name='correct_gender_enum',
                                               create_type=False),
                                        nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)


class MedCard(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        init=False,
        server_default=text("gen_random_uuid()")
    )
    patient_id: Mapped[str] = mapped_column()
    photo_url: Mapped[str]
    date_issue: Mapped[date]
    date_last_request: Mapped[datetime]
    date_next_visit: Mapped[datetime]
    number_insurance_policy: Mapped[str]
    date_expiration: Mapped[date]
    diagnosis: Mapped[str]
    disease_history: Mapped[str]

