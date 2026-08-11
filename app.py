from fastapi import FastAPI, Request
from models.almacen import miClaseBase, motor
from routers import becas, carreras, clases, login, usuarios, estudiantes, profesores, recursos_humanos, seguros, nomina, inscripciones

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles

miClaseBase.metadata.create_all(bind = motor)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/login", response_class= HTMLResponse)
def login_page(request: Request):
     return templates.TemplateResponse(request, 'login.html')
 
 
@app.get("/workspace", response_class= HTMLResponse)
def login_page(request: Request):
     return templates.TemplateResponse(request, 'workspace.html')


app.include_router(becas.router)
app.include_router(carreras.router)
app.include_router(clases.router)
app.include_router(usuarios.router)
app.include_router(estudiantes.router)
app.include_router(profesores.router)
app.include_router(recursos_humanos.router)
app.include_router(seguros.router)
app.include_router(nomina.router)
app.include_router(inscripciones.router)
app.include_router(login.router)