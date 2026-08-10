from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from models.almacen import miClaseBase, abrir_puerta_a_bd
from models.filtro_seguridad import RevisarBecas
from models.tablas import Becas
from utils.seguridad import el_vigilante, solo_administrador, administrador_o_profesor


router = APIRouter(
    prefix = "/becas",
    tags = ["Becas"]
)


@router.get("/")
def ver_listado_de_becas(
    info_user : dict = Depends(administrador_o_profesor),  
    base_datos: Session = Depends(abrir_puerta_a_bd)
):
    many = 0
    revisar = base_datos.query(Becas).all()
    
    if not revisar:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No hay becas registradas aun!"
        )
    else:
        for elemento in revisar:
            many += 1
        
        return {
            "Alerta": f"Se encontraron {many} becas",
            "Becas": revisar
        }
            
            
@router.get("/{id_url}")
def filtrar_por_id (
    id_url: int,  
    info_user : dict = Depends(administrador_o_profesor),  
    base_datos : Session = Depends(abrir_puerta_a_bd)
):
    check = base_datos.query(Becas).filter(Becas.id == id_url).first()
    
    if check is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"La beca con id: {id_url} no existe en el sistema"
        )
    else:
        return check

@router.post("/", status_code = status.HTTP_201_CREATED)
def crear_beca(
    json : RevisarBecas,  
    info_user: dict = Depends(solo_administrador),  
    base_datos: Session = Depends(abrir_puerta_a_bd)
):
    check = base_datos.query(Becas).filter(Becas.tipo_beca ==json.tipo_beca).first()
    
    if check is None:
        
        new_data = Becas(
            tipo_beca = json.tipo_beca,
            porcentaje_descuento = json.porcentaje_descuento,
            duracion = json.duracion  
        )
        base_datos.add(new_data)
        base_datos.commit()
        base_datos.refresh(new_data)
        return {
            "Atencion": f"{json.tipo_beca} registrada con exito",
            "ID Confirmacion": new_data.id
        }
    else:
        raise HTTPException(
            status_code =status.HTTP_409_CONFLICT,
            detail = f"{json.tipo_beca} ya se encuentra resgistrada. Te equivocaste?"
        )


@router.delete("/{id}")
def eliminar_por_id(
    id: int,
    info_user: dict = Depends(solo_administrador),  
    base_datos: Session= Depends(abrir_puerta_a_bd)
):
    check = base_datos.query(Becas).filter(Becas.id == id).first()
    if check is None:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail = f"Error, {id} de Beca no se encuentra en el sistema"
        )
    else:
        base_datos.delete(check)
        base_datos.commit()
        return{
            "Alerta": f"Beca con id  #{id} ha sido eliminada del sistema!"
        }


@router.put("/{id}")
def actualizar_beca(
    id: int,
    json: RevisarBecas,  
    info_user: dict = Depends(solo_administrador),  
    base_datos: Session = Depends(abrir_puerta_a_bd)
):
    check = base_datos.query(Becas).filter(Becas.id == id).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La beca con id {id} no existe"
        )
    
    check.tipo_beca = json.tipo_beca
    check.porcentaje_descuento = json.porcentaje_descuento
    check.duracion = json.duracion
    
    base_datos.commit()
    base_datos.refresh(check)
    
    return {
        "Alerta": f"Beca {id} actualizada correctamente",
        "beca": check
    }