from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

UBICACION_ALMACEN = os.getenv("UBICACION_ALMACEN")
motor = create_engine(UBICACION_ALMACEN)
llaves = sessionmaker(motor)
miClaseBase = DeclarativeBase()

def abrir_puerta_a_bd():
    try:
        base_datos = llaves()
        yield base_datos
    finally:
        base_datos.close()
        
