from fastapi import APIRouter, Depends
from app.controllers.librero_controller import LibreroController
from app.utils.auth_middleware import get_current_user

router = APIRouter()


@router.post("/libros/{id_libro}/prestar", tags=["Libros"])
async def prestar_libro(
        id_libro: int,
        current_user: dict = Depends(get_current_user)
):
    return LibreroController.agregar_libro_librero(current_user['id'], id_libro)


@router.post("/libros/{id_libro}/devolver", tags=["Libros"])
async def devolver_libro(
        id_libro: int,
        current_user: dict = Depends(get_current_user)
):
    return LibreroController.eliminar_libro_librero(current_user['id'], id_libro)