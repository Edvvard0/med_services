from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter(prefix='/pages',
                   tags=['Pages'])

template = Jinja2Templates(directory='app/templates')


@router.get('/')
async def info_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(name='index.html',
                                     context={'request': request})


@router.get("/login")
async def login_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(name='index.html',
                                     context={'request': request,
                                              'role': 'patient'})
