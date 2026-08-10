from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from models.almacen import abrir_puerta_a_bd
from models.filtro_seguridad import RevisarSeguros
from models.tablas import Seguros
from utils.seguridad import administrador_o_profesor, solo_administrador 

router = APIRouter(
    prefix="/seguros",
    tags=["Seguros"]
)

@router.get("/")
def ver_listado_de_seguros(
    info_user: dict = Depends(administrador_o_profesor),  
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    many = 0
    revisar = base_datos.query(Seguros).all()
    
    if not revisar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay seguros registrados aun!"
        )
    else:
        for elemento in revisar:
            many += 1
        return {
            "Alerta": f"Se encontraron {many} seguros",
            "Seguros": revisar
        }

@router.get("/{id_url}")
def filtrar_por_id(
    id_url: int,
    info_user: dict = Depends(administrador_o_profesor),  
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Seguros).filter(Seguros.id == id_url).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El seguro con id: {id_url} no existe en el sistema"
        )
    else:
        return check

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_seguro(
    json: RevisarSeguros,
    info_user: dict = Depends(solo_administrador),  
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Seguros).filter(Seguros.tipo_seguro == json.tipo_seguro).first()
    
    if check is None:
        new_data = Seguros(
            tipo_seguro=json.tipo_seguro,
            porcentaje_descuento=json.porcentaje_descuento,
            contrato=json.contrato
        )
        base_datos.add(new_data)
        base_datos.commit()
        base_datos.refresh(new_data)
        return {
            "Atencion": f"Seguro {json.tipo_seguro} registrado con exito",
            "ID Confirmacion": new_data.id
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Seguro {json.tipo_seguro} ya existe"
        )

@router.put("/{id}")
def actualizar_seguro(
    id: int,
    json: RevisarSeguros,
    info_user: dict = Depends(solo_administrador),  
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Seguros).filter(Seguros.id == id).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El seguro con id {id} no existe"
        )
    
    check.tipo_seguro = json.tipo_seguro
    check.porcentaje_descuento = json.porcentaje_descuento
    check.contrato = json.contrato
    
    base_datos.commit()
    base_datos.refresh(check)
    
    return {
        "Alerta": f"Seguro {id} actualizado correctamente",
        "seguro": check
    }

@router.delete("/{id}")
def eliminar_por_id(
    id: int,
    info_user: dict = Depends(solo_administrador),  
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Seguros).filter(Seguros.id == id).first()
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error, {id} de Seguro no se encuentra en el sistema"
        )
    else:
        base_datos.delete(check)
        base_datos.commit()
        return{
            "Alerta": f"Seguro con id #{id} ha sido eliminado del sistema!"
        }