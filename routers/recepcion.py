from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from models.almacen import abrir_puerta_a_bd  
from models.tablas import Usuarios           
from models.filtro_seguridad import RevisarLogin 
from utils.boletos import crear_boleto ,verificar_boleto  

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
    
    
    if check.password != json.password:
        raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail = f"Contrasena Incorrecta"
                )
    
  
    boleto = crear_boleto(check.id, check.user)
    
    return {
        "boleto": boleto,
        "user": check.user
    }
    

def el_vigilante(token: str = Header(...)):
    # 1. El vigilante recibe el 'token' que viene en el encabezado de la web
    
    # 2. verificar si el boleto es real
    datos_del_usuario = verificar_boleto(token)
    
    # 3. Si 'verificar_boleto' devuelve None, es que el boleto es falso o caduco
    if datos_del_usuario is None:
        raise HTTPException(status_code=401, detail="Boleto no valido")
    else:
        # 4. Si el boleto es real, el vigilante deja pasar (devuelve los datos)
          return datos_del_usuario
    
    
    