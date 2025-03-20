from fastapi import APIRouter, Depends, Query
from app.controllers.autor_controller import AutorController
from app.utils.auth_middleware import get_current_user
from app.schemas.autor import AutorCreate
router = APIRouter()

@router.get("/autores", tags=["Autores"])
async def obtener_autores(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    return AutorController.get_autores(page, limit)

@router.post("/autores", tags=["Autores"], status_code=201)
async def crear_autor(
    autor: AutorCreate,
    current_user: dict = Depends(get_current_user),
):
    return AutorController.create_autor(
        nombre=autor.nombre,
        apellido=autor.apellido,
        fecha_nacimiento=autor.fecha_nacimiento
    )