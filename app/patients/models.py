from datetime import date
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from app.database import Base


class CorrectGender(Enum):
    MAN: str = "man"
    WOMAN: str = "woman"


class Patient(Base):
    photo_url: Mapped[str]
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    patronymic: Mapped[str] = mapped_column(nullable=False)
    date_birthday: Mapped[date] = mapped_column(nullable=False)

    number_passport: Mapped[int] = mapped_column(nullable=False)
    series_passport: Mapped[int] = mapped_column(nullable=False)

    gender: Mapped[str] = mapped_column(PgEnum(CorrectGender,
                                               name='correct_gender_enum',
                                               create_type=False),
                                        nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[int] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
