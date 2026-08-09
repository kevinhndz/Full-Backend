from fastapi import FastAPI
from models.almacen import miClaseBase, motor
from routers import becas

miClaseBase.metadata.create_all(bind = motor)

app = FastAPI()

app.include_router(becas.router)
