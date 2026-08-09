from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from models.almacen import abrir_puerta_a_bd
from models.filtro_seguridad import RevisarNomina
from models.tablas import Nomina

router = APIRouter(
    prefix="/nomina",
    tags=["Nomina"]
)

@router.get("/")
def ver_listado_nomina(base_datos: Session = Depends(abrir_puerta_a_bd)):
    many = 0
    revisar = base_datos.query(Nomina).all()
    
    if not revisar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay nomina registrada aun!"
        )
    else:
        for elemento in revisar:
            many += 1
        return {
            "Alerta": f"Se encontraron {many} registros de nomina",
            "Nomina": revisar
        }

@router.get("/{id_url}")
def filtrar_por_id(id_url: int, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Nomina).filter(Nomina.id == id_url).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La nomina con id: {id_url} no existe en el sistema"
        )
    else:
        return check

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_nomina(json: RevisarNomina, base_datos: Session = Depends(abrir_puerta_a_bd)):
    new_data = Nomina(
        id_profesor=json.id_profesor,
        id_rrhh=json.id_rrhh
    )
    base_datos.add(new_data)
    base_datos.commit()
    base_datos.refresh(new_data)
    return {
        "Atencion": f"Nomina registrada con exito",
        "ID Confirmacion": new_data.id
    }

@router.put("/{id}")
def actualizar_nomina(id: int, json: RevisarNomina, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Nomina).filter(Nomina.id == id).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La nomina con id {id} no existe"
        )
    
    check.id_profesor = json.id_profesor
    check.id_rrhh = json.id_rrhh
    
    base_datos.commit()
    base_datos.refresh(check)
    
    return {
        "Alerta": f"Nomina {id} actualizada correctamente",
        "nomina": check
    }

@router.delete("/{id}")
def eliminar_por_id(id: int, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Nomina).filter(Nomina.id == id).first()
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error, {id} de Nomina no se encuentra en el sistema"
        )
    else:
        base_datos.delete(check)
        base_datos.commit()
        return{
            "Alerta": f"Nomina con id #{id} ha sido eliminada del sistema!"
        }

@router.get("/profesor/{id_profesor}")
def nomina_por_profesor(id_profesor: int, base_datos: Session = Depends(abrir_puerta_a_bd)):
    revisar = base_datos.query(Nomina).filter(Nomina.id_profesor == id_profesor).all()
    
    if not revisar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No hay nomina para el profesor {id_profesor}"
        )
    
    return {
        "total": len(revisar),
        "nomina": revisar
    }