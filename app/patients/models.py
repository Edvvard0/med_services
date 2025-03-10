import uuid
from datetime import date, datetime
from enum import Enum

from sqlalchemy import text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM as PgEnum, types

from app.database import Base


class CorrectGender(Enum):
    MAN: str = "man"
    WOMAN: str = "woman"


class Patient(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str] = mapped_column(nullable=True)
    date_birthday: Mapped[date] = mapped_column(nullable=False)

    passport: Mapped[str] = mapped_column(nullable=False)

    gender: Mapped[str] = mapped_column(PgEnum(CorrectGender,
                                               name='correct_gender_enum',
                                               create_type=False),
                                        nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)

    med_card_id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4,
    )
    photo_url: Mapped[str]
    date_issue: Mapped[date]
    date_last_request: Mapped[datetime]
    date_next_visit: Mapped[datetime]
    number_insurance_policy: Mapped[str]
    date_expiration: Mapped[date]
    diagnosis: Mapped[str]
    disease_history: Mapped[str]

    insurance_company: Mapped[str]

    password: Mapped[str]

    # insurance_company_id: Mapped[int] = mapped_column(Integer, ForeignKey("insurance_companies.id"))


class InsuranceCompanies(Base):
    __tablename__ = "insurance_companies"

    name: Mapped[str]
