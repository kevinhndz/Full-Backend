from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from models.almacen import abrir_puerta_a_bd
from models.filtro_seguridad import RevisarClases
from models.tablas import Clases

router = APIRouter(
    prefix="/clases",
    tags=["Clases"]
)

@router.get("/")
def ver_listado_de_clases(base_datos: Session = Depends(abrir_puerta_a_bd)):
    many = 0
    revisar = base_datos.query(Clases).all()
    
    if not revisar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay clases registradas aun!"
        )
    else:
        for elemento in revisar:
            many += 1
        return {
            "alerta": f"Se encontraron {many} clases",
            "Clases": revisar
        }

@router.get("/{id_url}")
def filtrar_por_id(id_url: int, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Clases).filter(Clases.id == id_url).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La clase con id: {id_url} no existe en el sistema"
        )
    else:
        return check

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_clase(json: RevisarClases, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Clases).filter(Clases.codigo == json.codigo).first()
    
    if check is None:
        new_data = Clases(
            nombre=json.nombre,
            creditos=json.creditos,
            codigo=json.codigo,
            modalidad=json.modalidad,
            dia=json.dia,
            horario=json.horario
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
            detail=f"Clase con código {json.codigo} ya existe"
        )

@router.put("/{id}")
def actualizar_clase(id: int, json: RevisarClases, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Clases).filter(Clases.id == id).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La clase con id {id} no existe"
        )
    
    check.nombre = json.nombre
    check.creditos = json.creditos
    check.codigo = json.codigo
    check.modalidad = json.modalidad
    check.dia = json.dia
    check.horario = json.horario
    
    base_datos.commit()
    base_datos.refresh(check)
    
    return {
        "Alerta": f"Clase {id} actualizada correctamente",
        "clase": check
    }

@router.delete("/{id}")
def eliminar_por_id(id: int, base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Clases).filter(Clases.id == id).first()
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error, {id} de Clase no se encuentra en el sistema"
        )
    else:
        base_datos.delete(check)
        base_datos.commit()
        return{
            "Alerta": f"Clase con id #{id} ha sido eliminada del sistema!"
        }