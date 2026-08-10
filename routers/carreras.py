from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from models.almacen import miClaseBase, abrir_puerta_a_bd
from models.filtro_seguridad import RevisarCarreras
from models.tablas import Carreras

from utils.seguridad import todos_pueden, solo_administrador

router = APIRouter(
    prefix="/carreras",
    tags=["Carreras"]
)

@router.get("/")
def ver_listado_de_carreras(info_user: dict = Depends(todos_pueden),base_datos: Session = Depends(abrir_puerta_a_bd)):
    many = 0
    revisar = base_datos.query(Carreras).all()
    
    if not revisar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay carreras registradas aun!"
        )
    else:
        for elemento in revisar:
            many += 1
        return {
            "Álerta": f"Se encontraron {many} carreras",
            "Carreras": revisar
        }

@router.get("/{id_url}")
def filtrar_por_id(id_url: int,info_user: dict = Depends(todos_pueden), base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Carreras).filter(Carreras.id == id_url).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La carrera con id: {id_url} no existe en el sistema"
        )
    else:
        return check

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_carrera(json: RevisarCarreras, info_user: dict = Depends(solo_administrador), base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Carreras).filter(Carreras.nombre == json.nombre).first()
    
    if check is None:
        new_data = Carreras(
            nombre=json.nombre,
            duracion=json.duracion,
            cantidad_clases=json.cantidad_clases
        )
        base_datos.add(new_data)
        base_datos.commit()
        base_datos.refresh(new_data)
        return {
            "Atencion": f"{json.nombre} registrada con exito",
            "ID Confirmacion": new_data.id
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{json.nombre} ya se encuentra registrada"
        )

@router.put("/{id}")
def actualizar_carrera(id: int, json: RevisarCarreras, info_user: dict = Depends(solo_administrador), base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Carreras).filter(Carreras.id == id).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La carrera con id {id} no existe"
        )
    
    check.nombre = json.nombre
    check.duracion = json.duracion
    check.cantidad_clases = json.cantidad_clases
    
    base_datos.commit()
    base_datos.refresh(check)
    
    return {
        "Alerta": f"Carrera {id} actualizada correctamente",
        "carrera": check
    }

@router.delete("/{id}")
def eliminar_por_id(id: int,info_user: dict = Depends(solo_administrador), base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Carreras).filter(Carreras.id == id).first()
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error, {id} de Carrera no se encuentra en el sistema"
        )
    else:
        base_datos.delete(check)
        base_datos.commit()
        return{
            "Alerta": f"Carrera con id #{id} ha sido eliminada del sistema!"
        }