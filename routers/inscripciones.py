from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from models.almacen import abrir_puerta_a_bd
from models.filtro_seguridad import (
    RevisarInsc_Estudiante_Clase,
    RevisarInsc_Profesor_Clase,
    RevisarInsc_Profesor_Carrera,
    RevisarInsc_Profesor_Seguro
)
from models.tablas import (
    Insc_Estudiante_Clase,
    Insc_Profesor_Clase,
    Insc_Profesor_Carrera,
    Insc_Profesor_Seguro
)
from utils.seguridad import administrador_o_profesor, solo_administrador  # ← AGREGAR

router = APIRouter(
    prefix="/inscripciones",
    tags=["Inscripciones"]
)

# ============= ESTUDIANTE - CLASE =============

@router.post("/estudiante-clase", status_code=status.HTTP_201_CREATED)
def inscribir_estudiante_clase(
    json: RevisarInsc_Estudiante_Clase,
    info_user: dict = Depends(administrador_o_profesor),  # ← AGREGAR
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Insc_Estudiante_Clase).filter(
        Insc_Estudiante_Clase.id_estudiante == json.id_estudiante,
        Insc_Estudiante_Clase.id_clase == json.id_clase
    ).first()
    
    if check is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Estudiante {json.id_estudiante} ya esta inscrito en clase {json.id_clase}"
        )
    
    new_data = Insc_Estudiante_Clase(
        id_estudiante=json.id_estudiante,
        id_clase=json.id_clase
    )
    base_datos.add(new_data)
    base_datos.commit()
    
    return {
        "Mensaje": "Estudiante inscrito en clase exitosamente"
    }

@router.get("/clase/{id_clase}")
def listar_estudiantes_por_clase(
    id_clase: int,
    info_user: dict = Depends(administrador_o_profesor),  # ← AGREGAR
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    revisar = base_datos.query(Insc_Estudiante_Clase).filter(Insc_Estudiante_Clase.id_clase == id_clase).all()
    
    if not revisar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No hay estudiantes inscritos en la clase {id_clase}"
        )
    
    return {
        "total": len(revisar),
        "inscripciones": revisar
    }

@router.get("/estudiante/{id_estudiante}")
def listar_clases_por_estudiante(
    id_estudiante: int,
    info_user: dict = Depends(administrador_o_profesor),  # ← AGREGAR
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    revisar = base_datos.query(Insc_Estudiante_Clase).filter(Insc_Estudiante_Clase.id_estudiante == id_estudiante).all()
    
    if not revisar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El estudiante {id_estudiante} no esta inscrito en ninguna clase"
        )
    
    return {
        "total": len(revisar),
        "inscripciones": revisar
    }

@router.delete("/estudiante-clase")
def desinscribir_estudiante_clase(
    json: RevisarInsc_Estudiante_Clase,
    info_user: dict = Depends(solo_administrador),  # ← AGREGAR
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Insc_Estudiante_Clase).filter(
        Insc_Estudiante_Clase.id_estudiante == json.id_estudiante,
        Insc_Estudiante_Clase.id_clase == json.id_clase
    ).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inscripcion no encontrada"
        )
    
    base_datos.delete(check)
    base_datos.commit()
    
    return {
        "Mensaje": "Estudiante desinscrito de la clase exitosamente"
    }

# ============= PROFESOR - CLASE =============

@router.post("/profesor-clase", status_code=status.HTTP_201_CREATED)
def asignar_profesor_clase(
    json: RevisarInsc_Profesor_Clase,
    info_user: dict = Depends(solo_administrador),  # ← AGREGAR
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Insc_Profesor_Clase).filter(
        Insc_Profesor_Clase.id_profesor == json.id_profesor,
        Insc_Profesor_Clase.id_clase == json.id_clase
    ).first()
    
    if check is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Profesor {json.id_profesor} ya esta asignado a la clase {json.id_clase}"
        )
    
    new_data = Insc_Profesor_Clase(
        id_profesor=json.id_profesor,
        id_clase=json.id_clase
    )
    base_datos.add(new_data)
    base_datos.commit()
    
    return {
        "Mensaje": "Profesor asignado a clase exitosamente"
    }

@router.delete("/profesor-clase")
def desasignar_profesor_clase(
    json: RevisarInsc_Profesor_Clase,
    info_user: dict = Depends(solo_administrador),  # ← AGREGAR
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Insc_Profesor_Clase).filter(
        Insc_Profesor_Clase.id_profesor == json.id_profesor,
        Insc_Profesor_Clase.id_clase == json.id_clase
    ).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asignacion no encontrada"
        )
    
    base_datos.delete(check)
    base_datos.commit()
    
    return {
        "Mensaje": "Profesor desasignado de la clase exitosamente"
    }

# ============= PROFESOR - CARRERA =============

@router.post("/profesor-carrera", status_code=status.HTTP_201_CREATED)
def asignar_profesor_carrera(
    json: RevisarInsc_Profesor_Carrera,
    info_user: dict = Depends(solo_administrador),  # ← AGREGAR
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Insc_Profesor_Carrera).filter(
        Insc_Profesor_Carrera.id_profesor == json.id_profesor,
        Insc_Profesor_Carrera.id_carrera == json.id_carrera
    ).first()
    
    if check is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Profesor {json.id_profesor} ya esta asignado a la carrera {json.id_carrera}"
        )
    
    new_data = Insc_Profesor_Carrera(
        id_profesor=json.id_profesor,
        id_carrera=json.id_carrera
    )
    base_datos.add(new_data)
    base_datos.commit()
    
    return {
        "Mensaje": "Profesor asignado a carrera exitosamente"
    }

@router.delete("/profesor-carrera")
def desasignar_profesor_carrera(
    json: RevisarInsc_Profesor_Carrera,
    info_user: dict = Depends(solo_administrador),  
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Insc_Profesor_Carrera).filter(
        Insc_Profesor_Carrera.id_profesor == json.id_profesor,
        Insc_Profesor_Carrera.id_carrera == json.id_carrera
    ).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asignacion no encontrada"
        )
    
    base_datos.delete(check)
    base_datos.commit()
    
    return {
        "Mensaje": "Profesor desasignado de la carrera exitosamente"
    }

# ============= PROFESOR - SEGURO =============

@router.post("/profesor-seguro", status_code=status.HTTP_201_CREATED)
def asignar_profesor_seguro(
    json: RevisarInsc_Profesor_Seguro,
    info_user: dict = Depends(administrador_o_profesor),  
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Insc_Profesor_Seguro).filter(
        Insc_Profesor_Seguro.id_profesor == json.id_profesor,
        Insc_Profesor_Seguro.id_seguro == json.id_seguro
    ).first()
    
    if check is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Profesor {json.id_profesor} ya tiene el seguro {json.id_seguro}"
        )
    
    new_data = Insc_Profesor_Seguro(
        id_profesor=json.id_profesor,
        id_seguro=json.id_seguro
    )
    base_datos.add(new_data)
    base_datos.commit()
    
    return {
        "Mensaje": "Seguro asignado a profesor exitosamente"
    }

@router.delete("/profesor-seguro")
def desasignar_profesor_seguro(
    json: RevisarInsc_Profesor_Seguro,
    info_user: dict = Depends(solo_administrador),  
    base_datos: Session = Depends(abrir_puerta_a_bd)):
    check = base_datos.query(Insc_Profesor_Seguro).filter(
        Insc_Profesor_Seguro.id_profesor == json.id_profesor,
        Insc_Profesor_Seguro.id_seguro == json.id_seguro
    ).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asignacion no encontrada"
        )
    
    base_datos.delete(check)
    base_datos.commit()
    
    return {
        "Mensaje": "Seguro desasignado del profesor exitosamente"
    }