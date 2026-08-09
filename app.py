from fastapi import FastAPI
from models.almacen import miClaseBase, motor
from routers import becas, carreras, clases, usuarios, estudiantes, profesores, recursos_humanos, seguros, nomina, inscripciones, recepcion
miClaseBase.metadata.create_all(bind = motor)

app = FastAPI()


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
app.include_router(recepcion.router)