from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Cabinet(Base):
    number_cabinet: Mapped[int]
    name: Mapped[int]
