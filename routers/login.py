from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from models.almacen import abrir_puerta_a_bd  
from models.tablas import Usuarios           
from models.filtro_seguridad import RevisarLogin 
from utils.boletos import crear_boleto ,verificar_boleto  

from utils.hash import verificar_contrasena

router = APIRouter(prefix="/recepcion", tags=["Recepcion"])

@router.post("/login")
def login(
    json: RevisarLogin,
    base_datos: Session = Depends(abrir_puerta_a_bd)
):
   
    check = base_datos.query(Usuarios).filter(Usuarios.user == json.user).first()
    
    if check is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Error el usuario: {json.user} no ha sido encontrado"
        )
    if not verificar_contrasena(json.password, check.password):
        raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail = f"Contrasena Incorrecta"
                )
    
  
    boleto = crear_boleto(check.id, check.user, check.rol)
    
    
    
    return {
        "boleto": boleto,
        "user": check.user,
        "rol": check.rol
    }

    
    