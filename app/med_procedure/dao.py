from app.dao.base import BaseDAO
from app.med_procedure.models import MedProcedure


class MedProcedureDAO(BaseDAO):
    model = MedProcedure

