from fastapi import APIRouter, Depends
from app.controllers.categoria_controller import CategoriaController
from app.utils.auth_middleware import get_current_user
from app.schemas.categoria import CategoriaCreate
router = APIRouter()


@router.get("/", tags=["Categorías"])
async def obtener_categorias(search: str = None, current_user: dict = Depends(get_current_user)):
    return CategoriaController.get_categorias(search)

@router.post("/", tags=["Categorías"], status_code=201)
async def crear_categoria(
    categoria: CategoriaCreate,
    current_user: dict = Depends(get_current_user)
):
    return CategoriaController.create_categoria(categoria.nombre)