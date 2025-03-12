from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.doctors.router import get_me_doc
from app.hospitalization.router import  get_lst_hosp_full_info
from app.patients.router import get_me, get_patient, all_patients

router = APIRouter(prefix='/pages',
                   tags=['Pages'])

template = Jinja2Templates(directory='app/templates')


@router.get('/')
async def info_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(name='index.html',
                                     context={'request': request})


@router.get("/login/patient")
async def login_patient_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(name='login.html',
                                     context={'request': request,
                                              'role': 'patient'})


@router.get("/patients/profile")
async def current_patient_page(request: Request, patient=Depends(get_me)) -> HTMLResponse:
    return template.TemplateResponse(
        name="patient_profile.html",
        context={'request': request,
                 'patient': patient}
    )


@router.get("/patients")
async def patients_page(request: Request, patients=Depends(all_patients)) -> HTMLResponse:
    return template.TemplateResponse(
        name="lst_patients.html",
        context={'request': request,
                 'patients': patients}
    )


@router.get("/patients/{patient_id}")
async def current_patient_page(request: Request, patient=Depends(get_patient)) -> HTMLResponse:
    return template.TemplateResponse(
        name="patient_profile.html",
        context={'request': request,
                 'patient': patient}
    )


@router.get("/login/doctor")
async def login_doctor_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(name='login.html',
                                     context={'request': request,
                                              'role': 'doctor'})


@router.get("/doctors/profile")
async def doctor_profile_page(request: Request, doctor=Depends(get_me_doc)) -> HTMLResponse:
    return template.TemplateResponse(name='main_doctor.html',
                                     context={'request': request,
                                              'doctor': doctor})


@router.get("/doctors/{doctor_id}")
async def current_doctor_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(name='login.html',
                                     context={'request': request,
                                              'role': 'doctor'})


@router.get("/hospitalizations")
async def hospitalizations_page(request: Request, lst_hosp=Depends(get_lst_hosp_full_info)) -> HTMLResponse:
    print(lst_hosp[0].patients)
    return template.TemplateResponse(name='lst_hosp.html',
                                     context={'request': request,
                                              "hospitalizations": lst_hosp})
