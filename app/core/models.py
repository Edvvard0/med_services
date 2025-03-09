from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Doctor(Base):
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str] = mapped_column(nullable=False)
    specialty: Mapped[str]


class InsuranceCompanies(Base):
    __tablename__ = "insurance_companies"

    name: Mapped[str]


class Cabinet(Base):
    number_cabinet: Mapped[int]
    name: Mapped[int]
