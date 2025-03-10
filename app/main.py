import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.patients.router import router as patient_router
from app.doctors.router import router as doctor_router
from app.hospitalization.router import router as hospitalization_router
from app.med_procedure.router import router as med_procedure_router
from app.pages.router import router as pages_router


app = FastAPI()

app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(hospitalization_router)
app.include_router(med_procedure_router)
app.include_router(pages_router)

app.mount("/static", StaticFiles(directory="app/static"), "static")


@app.get('/')
async def hello():
    return {"message": "hello"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
