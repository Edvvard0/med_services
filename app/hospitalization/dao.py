from app.dao.base import BaseDAO
from app.hospitalization.models import Hospitalization


class HospitalizationDAO(BaseDAO):
    model = Hospitalization
