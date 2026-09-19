from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
from contextlib import asynccontextmanager

# ----------------------------------------------------
# 1. MODELOS DE BASE DE DATOS (SQLModel)
# ----------------------------------------------------
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str

class Libro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    autor: str
    anio: int

# ----------------------------------------------------
# 2. CONEXIÓN A LA BASE DE DATOS (SQLite)
# ----------------------------------------------------
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=False)

def crear_tablas():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    yield

# ----------------------------------------------------
# 3. INICIALIZACIÓN DE LA API FASTAPI
# ----------------------------------------------------
app = FastAPI(
    title="API de Gestión de Usuarios y Libros",
    description="API RESTful sencilla desarrollada con FastAPI y SQLModel para despliegue en AWS EC2",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/", tags=["Inicio"])
def inicio():
    return {
        "mensaje": "¡Bienvenido a la API en AWS EC2!",
        "documentacion": "/docs"
    }

# ----------------------------------------------------
# 4. CRUD DE USUARIOS
# ----------------------------------------------------
@app.post("/usuarios/", response_model=Usuario, tags=["Usuarios"])
def crear_usuario(usuario: Usuario):
    with Session(engine) as session:
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario

@app.get("/usuarios/", response_model=List[Usuario], tags=["Usuarios"])
def listar_usuarios():
    with Session(engine) as session:
        usuarios = session.exec(select(Usuario)).all()
        return usuarios

@app.get("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuarios"])
def obtener_usuario(usuario_id: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario

@app.put("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuarios"])
def actualizar_usuario(usuario_id: int, datos: Usuario):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        usuario.nombre = datos.nombre
        usuario.email = datos.email
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario

@app.delete("/usuarios/{usuario_id}", tags=["Usuarios"])
def eliminar_usuario(usuario_id: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        session.delete(usuario)
        session.commit()
        return {"mensaje": f"Usuario con ID {usuario_id} eliminado exitosamente"}

# ----------------------------------------------------
# 5. CRUD DE LIBROS
# ----------------------------------------------------
@app.post("/libros/", response_model=Libro, tags=["Libros"])
def crear_libro(libro: Libro):
    with Session(engine) as session:
        session.add(libro)
        session.commit()
        session.refresh(libro)
        return libro

@app.get("/libros/", response_model=List[Libro], tags=["Libros"])
def listar_libros():
    with Session(engine) as session:
        libros = session.exec(select(Libro)).all()
        return libros

@app.get("/libros/{libro_id}", response_model=Libro, tags=["Libros"])
def obtener_libro(libro_id: int):
    with Session(engine) as session:
        libro = session.get(Libro, libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return libro

@app.put("/libros/{libro_id}", response_model=Libro, tags=["Libros"])
def actualizar_libro(libro_id: int, datos: Libro):
    with Session(engine) as session:
        libro = session.get(Libro, libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        libro.titulo = datos.titulo
        libro.autor = datos.autor
        libro.anio = datos.anio
        session.add(libro)
        session.commit()
        session.refresh(libro)
        return libro

@app.delete("/libros/{libro_id}", tags=["Libros"])
def eliminar_libro(libro_id: int):
    with Session(engine) as session:
        libro = session.get(Libro, libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        session.delete(libro)
        session.commit()
        return {"mensaje": f"Libro con ID {libro_id} eliminado exitosamente"}
