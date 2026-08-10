# Sistema de Gestion Universitaria (API REST)

Proyecto academico desarrollado con **FastAPI** y **SQLAlchemy** que administra la informacion de una universidad: estudiantes, profesores, carreras, clases, becas, seguros, nomina, recursos humanos y las inscripciones (relaciones muchos a muchos) entre estas entidades. El sistema cuenta con autenticacion basada en boletos (JWT) y control de acceso por roles (Administrador, Profesor, Estudiante).

## Tabla de contenido

1. [Archivos incluidos en la entrega](#archivos-incluidos-en-la-entrega)
2. [Descripcion general](#descripcion-general)
3. [Tecnologias usadas](#tecnologias-usadas)
4. [Estructura del proyecto](#estructura-del-proyecto)
5. [Esquema de la base de datos](#esquema-de-la-base-de-datos)
6. [Requisitos previos](#requisitos-previos)
7. [Instalacion paso a paso](#instalacion-paso-a-paso)
8. [Variables de entorno](#variables-de-entorno)
9. [Ejecutar el proyecto](#ejecutar-el-proyecto)
10. [Roles y autenticacion](#roles-y-autenticacion)
11. [Como probar los endpoints](#como-probar-los-endpoints)
12. [Documento de pruebas](#documento-de-pruebas-json-ejemplos)
13. [Modulos y endpoints disponibles](#modulos-y-endpoints-disponibles)
14. [Notas finales](#notas-finales)

---

## Archivos incluidos en la entrega

Cuando clones o descargues este proyecto, veras los siguientes archivos principales:

- **`README.md`** - Este archivo con toda la documentacion del proyecto
- **`Pruebas_API.docx`** - Documento Word con ejemplos de JSON para probar cada endpoint (descargalo para tener a mano durante las pruebas)
- **`db_hecha_a_mano.jpg`** - Imagen del boceto inicial del diseño de la base de datos (hecho en papel)
- **`dbpi.png`** - Diagrama final limpio de la base de datos con todas las relaciones
- **`universidad.db`** - Archivo de la base de datos SQLite con datos de prueba ya cargados (no elimines este archivo)
- **Carpetas del proyecto** (`models/`, `routers/`, `utils/`, etc) - El codigo fuente de la API

---

## Descripcion general

Esta API permite manejar de forma centralizada la operacion academica y administrativa de una universidad:

- Registro y consulta de **estudiantes**, **profesores** y personal de **recursos humanos**.
- Manejo de **carreras** y **clases**, incluyendo su relacion con estudiantes y profesores.
- Administracion de **becas** (asignadas a estudiantes) y **seguros** (asignados a profesores).
- Control de **nomina**, que vincula a un profesor con un registro de recursos humanos.
- Manejo de **inscripciones**, que son las tablas intermedias que resuelven las relaciones muchos a muchos (estudiante-clase, profesor-clase, profesor-carrera, profesor-seguro).
- Un modulo de **usuarios** y **login**, que emite un boleto (token JWT) usado para autenticar y autorizar cada peticion segun el rol del usuario.

Cada endpoint protegido valida el token en el header `token` y revisa el rol contenido dentro de ese token para decidir si el usuario puede o no ejecutar la accion solicitada.

## Tecnologias usadas

- Python 3.11+
- FastAPI
- Uvicorn (servidor ASGI)
- SQLAlchemy (ORM)
- SQLite (base de datos por defecto, definida en el `.env`)
- Pydantic (validacion de datos de entrada)
- python-jose (creacion y verificacion de JWT)
- python-dotenv (carga de variables de entorno)

## Estructura del proyecto

```
proyecto/
│
├── app.py                     # Punto de entrada, registra todos los routers
├── requirements.txt           # Dependencias del proyecto
├── .env                       # Variables de entorno (URL de la BD y llave secreta)
├── .gitignore
│
├── models/
│   ├── almacen.py             # Conexion a la base de datos (motor, sesiones)
│   ├── tablas.py              # Modelos ORM (tablas de la base de datos)
│   └── filtro_seguridad.py    # Esquemas Pydantic para validar los JSON de entrada
│
├── routers/
│   ├── login.py                # Endpoint de autenticacion (genera el boleto)
│   ├── usuarios.py             # CRUD de usuarios
│   ├── estudiantes.py          # CRUD de estudiantes
│   ├── profesores.py           # CRUD de profesores
│   ├── carreras.py             # CRUD de carreras
│   ├── clases.py               # CRUD de clases
│   ├── becas.py                # CRUD de becas
│   ├── seguros.py              # CRUD de seguros
│   ├── nomina.py                # CRUD de nomina
│   ├── recursos_humanos.py     # CRUD de recursos humanos
│   └── inscripciones.py        # Manejo de tablas intermedias (N:M)
│
└── utils/
    ├── seguridad.py            # Dependencias de autorizacion por rol
    └── boletos.py               # Creacion y verificacion del JWT
```

> Nota: en el codigo, los `import` usan las rutas `models.` y `utils.`, por lo que la carpeta debe respetar exactamente esa estructura para que el proyecto levante sin errores.

## Esquema de la base de datos

A continuacion el boceto original en el que se penso el modelo relacional (papel), y despues el diagrama ya limpio con el que quedo construida la base de datos final.

**Boceto inicial (diseño a mano):**

![Diseño a mano de la base de datos](/img/db_hecha_a_mano.jpg)

**Diagrama final de la base de datos:**

![Diagrama final de la base de datos](/img/dbpi.png)

Resumen de las relaciones principales:

- `Usuarios` 1:1 `Estudiantes` / `Profesores` / `RecursosHumanos` (cada persona tiene una cuenta de usuario).
- `Becas` 1:N `Estudiantes` (un estudiante tiene una beca, una beca puede tener varios estudiantes).
- `Carreras` 1:N `Estudiantes`.
- `Profesores` 1:N `Nomina` y `RecursosHumanos` 1:N `Nomina`.
- `Estudiantes` N:M `Clases` a traves de `Inscripcion_Estudiante_Clase`.
- `Profesores` N:M `Clases` a traves de `Inscripcion_Profesor_Clase`.
- `Profesores` N:M `Carreras` a traves de `Inscripcion_Profesor_Carrera`.
- `Profesores` N:M `Seguros` a traves de `Inscripcion_Profesor_Seguro`.

## Requisitos previos

Antes de clonar el repositorio se debe tener instalado:

- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Git

Se puede verificar con:

```bash
python --version
pip --version
git --version
```

## Instalacion paso a paso

1. **Clonar el repositorio**

```bash
git clone <URL-del-repositorio>
cd <nombre-de-la-carpeta-del-proyecto>
```

2. **Crear un entorno virtual**

```bash
python -m venv venv
```

3. **Activar el entorno virtual**

En Windows:

```bash
venv\Scripts\activate
```

En Mac / Linux:

```bash
source venv/bin/activate
```

4. **Instalar las dependencias**

```bash
pip install -r requirements.txt
```

> El paquete `python-jose` se usa para los boletos (JWT). Si al levantar el proyecto sale un error de tipo `ModuleNotFoundError: No module named 'jose'`, instalarlo manualmente con:
> ```bash
> pip install python-jose
> ```



 **Crear el archivo `.env`**
El archivo `.env` no viene en el repositorio por razones de seguridad (aunque si descargaras el `.gitignore`, que es parte del repo, veras que `.env` esta listado ahi para protegerlo). 
 
Debes crear manualmente un archivo llamado `.env` en la raiz del proyecto (en la misma carpeta donde esta `app.py`) y agregar estas dos lineas:
 
```
UBICACION_ALMACEN = "sqlite:///./universidad.db"
SECRET_KEY = "ExampleSecretKey32CharactersLong!"
```
 
> **Nota:** La `SECRET_KEY` debe tener minimo 32 caracteres.
 
La base de datos (`universidad.db`) ya viene prepoblada con datos de prueba (usuarios, estudiantes, profesores, carreras, clases, etc), por lo que no necesitas crear nada manualmente en la BD: esta lista para probar.

## Ejecutar el proyecto

Con el entorno virtual activado, se corre:

```bash
uvicorn app:app --reload
```

Si todo esta correcto, el servidor queda disponible en:

```
http://127.0.0.1:8000
```

Documentacion interactiva (Swagger) generada automaticamente por FastAPI:

```
http://127.0.0.1:8000/docs
```

Documentacion alterna (Redoc):

```
http://127.0.0.1:8000/redoc
```

## Roles y autenticacion

El sistema maneja **tres roles**:

- `Administrador`
- `Profesor`
- `Estudiante`

Cada rol tiene permisos distintos sobre los endpoints. Por ejemplo, crear o eliminar usuarios solo lo puede hacer un Administrador, mientras que ver el listado de clases lo puede hacer tanto Administrador como Profesor.

**Recomendacion para las pruebas:** iniciar sesion primero con un usuario de rol Administrador, ya que este rol es el unico que tiene acceso a la totalidad de los endpoints. Con ese boleto se pueden probar practicamente todos los modulos sin tener que estar cambiando de usuario a cada rato. Ya despues, si se quiere validar que las restricciones de rol funcionan, se inicia sesion con un usuario Profesor o Estudiante y se intenta acceder a un endpoint restringido para confirmar que responde con error 403.

### Como iniciar sesion

Endpoint: `POST /recepcion/login`

Body de ejemplo:

```json
{
  "user": "admin1",
  "password": "admin1234"
}
```

La respuesta entrega un boleto:

```json
{
  "boleto": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": "admin1",
  "rol": "Administrador"
}
```

### Como usar el boleto

Ese valor de `boleto` se debe copiar completo y enviarlo en el header `token` en cada peticion a un endpoint protegido:

```
token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

En Swagger (`/docs`) no hay boton de "Authorize" configurado para este header, asi que el token se pega manualmente en el campo `token` que aparece dentro de cada endpoint al momento de probarlo ("Try it out"). Si se usa Postman o Insomnia, se agrega como header normal con clave `token` y valor el boleto.

El boleto expira **30 minutos** despues de haberse generado. Si despues de un rato empieza a marcar error 401, es porque el boleto vencio y hay que volver a hacer login.

## Como probar los endpoints

1. Levantar el proyecto con `uvicorn app:app --reload`.
2. Entrar a `http://127.0.0.1:8000/docs`.
3. Ejecutar `POST /recepcion/login` con un usuario Administrador (usuario: `admin1`, contraseña: `admin1234`).
4. Copiar el valor de `boleto` de la respuesta.
5. En cada endpoint que se quiera probar, pegar ese valor en el campo `token`.
6. Ejecutar el endpoint (GET, POST, PUT o DELETE segun corresponda).

## Documento de Pruebas (JSON ejemplos)

Se incluye un documento Word llamado **`Pruebas_API.docx`** que contiene ejemplos de JSON listos para copiar y pegar en cada endpoint de creacion y actualizacion. El documento esta organizado por modulo y muestra:

- La URL del endpoint
- El metodo HTTP (GET, POST, PUT, DELETE)
- El rol requerido para ejecutar ese endpoint
- El JSON de ejemplo que se debe enviar en el body

**Descargar:** `Pruebas_API.docx`

Este documento es especialmente util porque permite trabajar mas rapido durante las pruebas sin tener que escribir manualmente cada JSON, y sirve como referencia rapida de la estructura de datos que acepta cada endpoint.

## Modulos y endpoints disponibles

| Modulo | Prefijo | Descripcion |
|---|---|---|
| Recepcion | `/recepcion` | Login y generacion del boleto |
| Usuarios | `/usuarios` | CRUD de cuentas de usuario |
| Estudiantes | `/estudiantes` | CRUD de estudiantes |
| Profesores | `/profesores` | CRUD de profesores |
| Carreras | `/carreras` | CRUD de carreras |
| Clases | `/clases` | CRUD de clases |
| Becas | `/becas` | CRUD de becas |
| Seguros | `/seguros` | CRUD de seguros |
| Nomina | `/nomina` | CRUD de nomina, incluye consulta por profesor |
| Recursos Humanos | `/rrhh` | CRUD de personal de recursos humanos |
| Inscripciones | `/inscripciones` | Maneja las relaciones N:M (estudiante-clase, profesor-clase, profesor-carrera, profesor-seguro) |

Cada modulo (excepto login) sigue el mismo patron de operaciones:

- `GET /` : lista todos los registros
- `GET /{id}` : busca un registro por id
- `POST /` : crea un registro nuevo
- `PUT /{id}` : actualiza un registro existente
- `DELETE /{id}` : elimina un registro

## Notas finales

- La base de datos usada por defecto es SQLite, por lo que no se necesita instalar ningun motor de base de datos aparte para probar el proyecto.
- Si se elimina el archivo `universidad.db`, la base de datos se vuelve a crear vacia la proxima vez que se corra el proyecto (gracias a `miClaseBase.metadata.create_all` en `app.py`), pero se pierde toda la informacion de prueba, por lo que habria que volver a registrar usuarios, carreras, clases, etc. manualmente antes de poder iniciar sesion.
- Los codigos de error mas comunes durante las pruebas son: `401` (token invalido o vencido), `403` (el rol del usuario no tiene permiso para ese endpoint), `404` (el registro no existe) y `409` (el registro ya existe, por ejemplo un correo o codigo duplicado).