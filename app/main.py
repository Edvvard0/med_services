import uvicorn
from fastapi import FastAPI
from app.patients.router import router as patient_router


app = FastAPI()

app.include_router(patient_router)

@app.get('/')
async def hello():
    return {"message": "hello"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
