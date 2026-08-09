from sqlalchemy import Integer, String, ForeignKey, Column, Float
from models.almacen import MiClaseBase  
from sqlalchemy.orm import relationship


class Usuarios(MiClaseBase):
    __tablename__ = "Usuarios"
    
    id = Column(Integer, primary_key=True)
    user = Column(String, unique=True)
    password = Column(String)
    rol = Column(String)
    
    estudiantes = relationship("Estudiantes", back_populates="usuario")
    profesores = relationship("Profesores", back_populates="usuario")
    recursoshumanos = relationship("RecursosHumanos", back_populates="usuario")


class Becas(MiClaseBase):
    __tablename__ = "Becas"
    
    id = Column(Integer, primary_key=True)
    tipo_beca = Column(String)
    porcentaje_descuento = Column(Float)
    duracion = Column(Integer)
    
    
    estudiantes = relationship("Estudiantes", back_populates="beca")


class Carreras(MiClaseBase):
    __tablename__ = "Carreras"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    duracion = Column(String)
    cantidad_clases = Column(Integer)
    
    
    estudiantes = relationship("Estudiantes", back_populates="carrera")
    profesores = relationship("Insc_Profesor_Carrera", back_populates="carrera")


class Clases(MiClaseBase):
    __tablename__ = "Clases"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    creditos = Column(Integer)
    codigo = Column(String)
    modalidad = Column(String)
    dia = Column(String)
    horario = Column(String)
    

    estudiantes = relationship("Insc_Estudiante_Clase", back_populates="clase")
    profesores = relationship("Insc_Profesor_Clase", back_populates="clase")


class Seguros(MiClaseBase):
    __tablename__ = "Seguros"
    
    id = Column(Integer, primary_key=True)
    tipo_seguro = Column(String)
    porcentaje_descuento = Column(Float)
    contrato = Column(String)
    
   
    profesores = relationship("Insc_Profesor_Seguro", back_populates="seguro")


class Estudiantes(MiClaseBase):
    __tablename__ = "Estudiantes"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    telefono = Column(String)
    cuenta = Column(String, unique=True)
    correo = Column(String, unique=True)
    direccion = Column(String)
    estado_civil = Column(String)
    edad = Column(Integer)
    modalidad = Column(String)
    
    id_beca = Column(Integer, ForeignKey("Becas.id"))
    id_carrera = Column(Integer, ForeignKey("Carreras.id"))
    id_usuario = Column(Integer, ForeignKey("Usuarios.id"))
    
    
    beca = relationship("Becas", back_populates="estudiantes")
    carrera = relationship("Carreras", back_populates="estudiantes")
    usuario = relationship("Usuarios", back_populates="estudiantes")
   
    clases = relationship("Insc_Estudiante_Clase", back_populates="estudiante")


class Profesores(MiClaseBase):
    __tablename__ = "Profesores"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    telefono = Column(String)
    correo = Column(String, unique=True)
    direccion = Column(String)
    estado_civil = Column(String)
    edad = Column(Integer)
    modalidad = Column(String)
    codigo_empleado = Column(String, unique=True)
    salario = Column(Float)
    
    
    id_usuario = Column(Integer, ForeignKey("Usuarios.id"))
    
    # Relaciones
    usuario = relationship("Usuarios", back_populates="profesores")
    clases = relationship("Insc_Profesor_Clase", back_populates="profesor")
    carreras = relationship("Insc_Profesor_Carrera", back_populates="profesor")
    seguros = relationship("Insc_Profesor_Seguro", back_populates="profesor")
    nomina = relationship("Nomina", back_populates="profesor")


class RecursosHumanos(MiClaseBase):
    __tablename__ = "RecursosHumanos"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    telefono = Column(String)
    correo = Column(String, unique=True)
    direccion = Column(String)
    codigo_empleado = Column(Integer, unique=True)
    

    id_usuario = Column(Integer, ForeignKey("Usuarios.id"))
    
    # Relaciones
    usuario = relationship("Usuarios", back_populates="recursoshumanos")
    nomina = relationship("Nomina", back_populates="rrhh")


class Nomina(MiClaseBase):
    __tablename__ = "Nomina"
    
    id = Column(Integer, primary_key=True)
    
 
    id_profesor = Column(Integer, ForeignKey("Profesores.id"))
    id_rrhh = Column(Integer, ForeignKey("RecursosHumanos.id"))
    
    # Relaciones
    profesor = relationship("Profesores", back_populates="nomina")
    rrhh = relationship("RecursosHumanos", back_populates="nomina")


# ===== TABLAS DE INTERSECCIONES (MUCHOS A MUCHOS) =====

class Insc_Estudiante_Clase(MiClaseBase):
    __tablename__ = "Inscripcion_Estudiante_Clase"  
    
    id = Column(Integer, primary_key=True)
    
   
    id_estudiante = Column(Integer, ForeignKey("Estudiantes.id"))
    id_clase = Column(Integer, ForeignKey("Clases.id"))
    
    # Relaciones
    estudiante = relationship("Estudiantes", back_populates="clases")
    clase = relationship("Clases", back_populates="estudiantes")


class Insc_Profesor_Clase(MiClaseBase):
    __tablename__ = "Inscripcion_Profesor_Clase"  
    
    id = Column(Integer, primary_key=True)
    
  
    id_profesor = Column(Integer, ForeignKey("Profesores.id"))
    id_clase = Column(Integer, ForeignKey("Clases.id"))
    
    # Relaciones
    profesor = relationship("Profesores", back_populates="clases")
    clase = relationship("Clases", back_populates="profesores")


class Insc_Profesor_Carrera(MiClaseBase):
    __tablename__ = "Inscripcion_Profesor_Carrera"  
    
    id = Column(Integer, primary_key=True)
    
    
    id_profesor = Column(Integer, ForeignKey("Profesores.id"))
    id_carrera = Column(Integer, ForeignKey("Carreras.id"))
    
    # Relaciones
    profesor = relationship("Profesores", back_populates="carreras")
    carrera = relationship("Carreras", back_populates="profesores")


class Insc_Profesor_Seguro(MiClaseBase):  
    __tablename__ = "Inscripcion_Profesor_Seguro"
    
    id = Column(Integer, primary_key=True)
    
    
    id_profesor = Column(Integer, ForeignKey("Profesores.id"))
    id_seguro = Column(Integer, ForeignKey("Seguros.id"))
    
    # Relaciones
    profesor = relationship("Profesores", back_populates="seguros")
    seguro = relationship("Seguros", back_populates="profesores")
