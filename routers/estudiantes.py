from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from models.almacen import abrir_puerta_a_bd
from models.filtro_seguridad import RevisarEstudiantes
from models.tablas import Estudiantes

router = APIRouter(
    prefix="/estudiantes",
    tags=["Estudiantes"]
)

@router.get("/")
def ver_listado_de_estudiantes(base_datos: Session = Depends(abrir_puerta_a_bd)):
    many = 0
    revisar = base_datos.query(Estudiantes).all()
    
    if not revisar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay estudiantes registrados aun!"
        )
    else:
        for elemento in revisar:
            many += 1
        return {
            "Alerta": f"Se encontraron {many} estudiantes",
            "Estudiantes": revisar
        }

@router.get("/{id_url}")
def filtrar_por_id(id_url: int, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Estudiantes).filter(Estudiantes.id == id_url).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El estudiante con id: {id_url} no existe en el sistema"
        )
    else:
        return check

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_estudiante(json: RevisarEstudiantes, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check_cuenta = base_datos.query(Estudiantes).filter(Estudiantes.cuenta == json.cuenta).first()
    check_correo = base_datos.query(Estudiantes).filter(Estudiantes.correo == json.correo).first()
    
    if check_cuenta is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cuenta {json.cuenta} ya existe"
        )
    
    if check_correo is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Correo {json.correo} ya existe"
        )
    
    new_data = Estudiantes(
        nombre=json.nombre,
        telefono=json.telefono,
        cuenta=json.cuenta,
        correo=json.correo,
        direccion=json.direccion,
        estado_civil=json.estado_civil,
        edad=json.edad,
        modalidad=json.modalidad,
        id_beca=json.id_beca,
        id_carrera=json.id_carrera,
        id_usuario=json.id_usuario
    )
    base_datos.add(new_data)
    base_datos.commit()
    base_datos.refresh(new_data)
    return {
        "Atencion": f"Estudiante {json.nombre} registrado con exito",
        "ID Confirmacion": new_data.id
    }

@router.put("/{id}")
def actualizar_estudiante(id: int, json: RevisarEstudiantes, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Estudiantes).filter(Estudiantes.id == id).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El estudiante con id {id} no existe"
        )
    
    check.nombre = json.nombre
    check.telefono = json.telefono
    check.cuenta = json.cuenta
    check.correo = json.correo
    check.direccion = json.direccion
    check.estado_civil = json.estado_civil
    check.edad = json.edad
    check.modalidad = json.modalidad
    check.id_beca = json.id_beca
    check.id_carrera = json.id_carrera
    check.id_usuario = json.id_usuario
    
    base_datos.commit()
    base_datos.refresh(check)
    
    return {
        "Alerta": f"Estudiante {id} actualizado correctamente",
        "estudiante": check
    }

@router.delete("/{id}")
def eliminar_por_id(id: int, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Estudiantes).filter(Estudiantes.id == id).first()
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error, {id} de Estudiante no se encuentra en el sistema"
        )
    else:
        base_datos.delete(check)
        base_datos.commit()
        return{
            "Alerta": f"Estudiante con id #{id} ha sido eliminado del sistema!"
        }