from fastapi import HTTPException, status, Header, Depends
from sqlalchemy.orm import Session
from utils.boletos import verificar_boleto


#Funcion Padre

def el_vigilante(token: str = Header(...)):
    
    datos_del_usuario = verificar_boleto(token)
    
    if datos_del_usuario is None:
        raise HTTPException(status_code=401, detail="Boleto no valido")
    else:
        return datos_del_usuario



def solo_administrador(info_user: dict = Depends(el_vigilante)):
   
    if info_user["rol"] != "Administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden acceder a esto"
        )
    return info_user


def solo_profesor(info_user: dict = Depends(el_vigilante)):
    
    if info_user["rol"] != "Profesor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo profesores pueden acceder a esto"
        )
    return info_user


def solo_estudiante(info_user: dict = Depends(el_vigilante)):
    
    if info_user["rol"] != "Estudiante":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo estudiantes pueden acceder a esto"
        )
    return info_user


def administrador_o_profesor(info_user: dict = Depends(el_vigilante)):
    if info_user["rol"] not in ["Administrador", "Profesor"]:
        raise HTTPException(status_code=403, detail="No permitido")
    return info_user

def estudiante_o_administrador(info_user: dict = Depends(el_vigilante)):
    
    if info_user["rol"] not in ["Estudiante, Profesor"]:
        raise HTTPException(status_code= 403, detail="No permitido")
    else:
        return info_user
    
def todos_pueden(info_user: dict = Depends(el_vigilante)):
    if info_user ["rol"] not in ["Administrador, Profesor, Estudiante"]:
        raise HTTPException(status_code= 403, detail="No permitido")
    else:
        return info_user
        
    