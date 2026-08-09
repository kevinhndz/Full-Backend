from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class RevisarUsuarios(BaseModel):
    user: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=8, max_length=25)
    rol: str = Field(min_length=5, max_length=20)


class RevisarBecas(BaseModel):
    tipo_beca: str = Field(min_length=5, max_length=50)
    porcentaje_descuento: float = Field(ge=0, le=100)
    duracion: int = Field(ge=1)


class RevisarCarreras(BaseModel):
    nombre: str = Field(min_length=5, max_length=100)
    duracion: str = Field(min_length=2, max_length=50)
    cantidad_clases: int = Field(ge=1)


class RevisarClases(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    creditos: int = Field(ge=1, le=10)
    codigo: str = Field(min_length=3, max_length=20)
    modalidad: str = Field(min_length=3, max_length=50)
    dia: str = Field(min_length=3, max_length=20)
    horario: str = Field(min_length=4, max_length=20)


class RevisarSeguros(BaseModel):
    tipo_seguro: str = Field(min_length=5, max_length=100)
    porcentaje_descuento: float = Field(ge=0, le=100)
    contrato: str = Field(min_length=5, max_length=100)


class RevisarEstudiantes(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    telefono: str = Field(min_length=7, max_length=20)
    cuenta: str = Field(min_length=5, max_length=50)
    correo: EmailStr
    direccion: str = Field(min_length=5, max_length=150)
    estado_civil: str = Field(min_length=5, max_length=20)
    edad: int = Field(ge=17, le=80)
    modalidad: str = Field(min_length=3, max_length=50)
    id_beca: Optional[int] = None
    id_carrera: int
    id_usuario: int


class RevisarProfesores(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    telefono: str = Field(min_length=7, max_length=20)
    correo: EmailStr
    direccion: str = Field(min_length=5, max_length=150)
    estado_civil: str = Field(min_length=5, max_length=20)
    edad: int = Field(ge=20, le=75)
    modalidad: str = Field(min_length=3, max_length=50)
    codigo_empleado: str = Field(min_length=5, max_length=50)
    salario: float = Field(ge=0)
    id_usuario: int


class RevisarRecursosHumanos(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    telefono: str = Field(min_length=7, max_length=20)
    correo: EmailStr
    direccion: str = Field(min_length=5, max_length=150)
    codigo_empleado: int = Field(ge=1)
    id_usuario: int


class RevisarNomina(BaseModel):
    id_profesor: int
    id_rrhh: int


class RevisarInsc_Estudiante_Clase(BaseModel):
    id_estudiante: int
    id_clase: int


class RevisarInsc_Profesor_Clase(BaseModel):
    id_profesor: int
    id_clase: int


class RevisarInsc_Profesor_Carrera(BaseModel):
    id_profesor: int
    id_carrera: int


class RevisarInsc_Profesor_Seguro(BaseModel):
    id_profesor: int
    id_seguro: int