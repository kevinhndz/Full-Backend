from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from models.almacen import abrir_puerta_a_bd
from models.filtro_seguridad import RevisarRecursosHumanos
from models.tablas import RecursosHumanos

router = APIRouter(
    prefix="/rrhh",
    tags=["Recursos Humanos"]
)

@router.get("/")
def ver_listado_rrhh(base_datos: Session = Depends(abrir_puerta_a_bd)):
    many = 0
    revisar = base_datos.query(RecursosHumanos).all()
    
    if not revisar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay RRHH registrados aun!"
        )
    else:
        for elemento in revisar:
            many += 1
        return {
            "alerta": f"Se encontraron {many} RRHH",
            "RRHH": revisar
        }

@router.get("/{id_url}")
def filtrar_por_id(id_url: int, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(RecursosHumanos).filter(RecursosHumanos.id == id_url).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El RRHH con id: {id_url} no existe en el sistema"
        )
    else:
        return check

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_rrhh(json: RevisarRecursosHumanos, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check_correo = base_datos.query(RecursosHumanos).filter(RecursosHumanos.correo == json.correo).first()
    check_empleado = base_datos.query(RecursosHumanos).filter(RecursosHumanos.codigo_empleado == json.codigo_empleado).first()
    
    if check_correo is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Correo {json.correo} ya existe"
        )
    
    if check_empleado is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Codigo de empleado {json.codigo_empleado} ya existe"
        )
    
    new_data = RecursosHumanos(
        nombre=json.nombre,
        telefono=json.telefono,
        correo=json.correo,
        direccion=json.direccion,
        codigo_empleado=json.codigo_empleado,
        id_usuario=json.id_usuario
    )
    base_datos.add(new_data)
    base_datos.commit()
    base_datos.refresh(new_data)
    return {
        "Atencion": f"RRHH {json.nombre} registrado con exito",
        "ID Confirmacion": new_data.id
    }

@router.put("/{id}")
def actualizar_rrhh(id: int, json: RevisarRecursosHumanos, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(RecursosHumanos).filter(RecursosHumanos.id == id).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El RRHH con id {id} no existe"
        )
    
    check.nombre = json.nombre
    check.telefono = json.telefono
    check.correo = json.correo
    check.direccion = json.direccion
    check.codigo_empleado = json.codigo_empleado
    check.id_usuario = json.id_usuario
    
    base_datos.commit()
    base_datos.refresh(check)
    
    return {
        "Alerta": f"RRHH {id} actualizado correctamente",
        "rrhh": check
    }

@router.delete("/{id}")
def eliminar_por_id(id: int, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(RecursosHumanos).filter(RecursosHumanos.id == id).first()
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error, {id} de RRHH no se encuentra en el sistema"
        )
    else:
        base_datos.delete(check)
        base_datos.commit()
        return{
            "Alerta": f"RRHH con id #{id} ha sido eliminado del sistema!"
        }