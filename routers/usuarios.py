from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from models.almacen import abrir_puerta_a_bd
from models.filtro_seguridad import RevisarUsuarios, RevisarLogin
from models.tablas import Usuarios
from utils.boletos import crear_boleto, verificar_boleto
from utils.seguridad import solo_administrador  

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.get("/")
def ver_listado_de_usuarios(
    info_user: dict = Depends(solo_administrador),  
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    many = 0
    revisar = base_datos.query(Usuarios).all()
    
    if not revisar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay usuarios registrados aun!"
        )
    else:
        for elemento in revisar:
            many += 1
        return {
            "Alerta": f"Se encontraron {many} usuarios",
            "Usuarios": revisar
        }

@router.get("/{id_url}")
def filtrar_por_id(
    id_url: int,
    info_user: dict = Depends(solo_administrador),  
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Usuarios).filter(Usuarios.id == id_url).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario con id: {id_url} no existe en el sistema"
        )
    else:
        return check

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_usuario(
    json: RevisarUsuarios,
    info_user: dict = Depends(solo_administrador),  
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Usuarios).filter(Usuarios.user == json.user).first()
    
    if check is None:
        new_data = Usuarios(
            user=json.user,
            password=json.password,
            rol=json.rol
        )
        base_datos.add(new_data)
        base_datos.commit()
        base_datos.refresh(new_data)
        return {
            "Atencion": f"Usuario {json.user} registrado con exito",
            "ID Confirmacion": new_data.id
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Usuario {json.user} ya existe"
        )

@router.put("/{id}")
def actualizar_usuario(
    id: int,
    json: RevisarUsuarios,
    info_user: dict = Depends(solo_administrador),  
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Usuarios).filter(Usuarios.id == id).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario con id {id} no existe"
        )
    
    check.user = json.user
    check.password = json.password
    check.rol = json.rol
    
    base_datos.commit()
    base_datos.refresh(check)
    
    return {
        "Alerta": f"Usuario {id} actualizado correctamente",
        "usuario": check
    }

@router.delete("/{id}")
def eliminar_por_id(
    id: int,
    info_user: dict = Depends(solo_administrador),  
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Usuarios).filter(Usuarios.id == id).first()
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error, {id} de Usuario no se encuentra en el sistema"
        )
    else:
        base_datos.delete(check)
        base_datos.commit()
        return{
            "Alerta": f"Usuario con id #{id} ha sido eliminado del sistema!"
        }
    
    
