from pydantic import BaseModel


class SDoctor(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    specialty: str
