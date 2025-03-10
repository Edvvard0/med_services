from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base





class InsuranceCompanies(Base):
    __tablename__ = "insurance_companies"

    name: Mapped[str]


class Cabinet(Base):
    number_cabinet: Mapped[int]
    name: Mapped[int]
