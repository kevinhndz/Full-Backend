from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

#imports de Modulo Models (base datos)
from models.almacen import miClaseBase, abrir_puerta_a_bd
from models.filtro_seguridad import RevisarBecas
from models.tablas import Becas


router = APIRouter(
    prefix = "/becas",
    tags = ["Becas"]
    
)


@router.get("/")
def ver_listado_de_becas(
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
            
            "Älerta": f"Se encontraron {many} becas",
            "Becas": revisar
        }
            
            
@router.get("/{id_url}")
def filtrar_por_id (
    
    id_url: int,
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
