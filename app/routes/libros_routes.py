import httpx
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.openapi.models import Response

from app.controllers.libro_controller import LibroController
from app.schemas.libro import LibroCreate
from app.utils.auth_middleware import get_current_user
import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

API_KEY = os.getenv("ADMIN_API_KEY")
BUCKET = os.getenv("S3_BUCKET")
s3 = boto3.client('s3')

def verificar_api_key(api_key: str = Header(..., alias="X-API-Key")):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Configuración de API Key faltante")

    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="API Key inválida")
    return True


# ========== Rutas Libros ==========
@router.get("/", tags=["Libros"])
async def obtener_libros_paginados(
        page: int = 1,
        limit: int = 50,
        current_user: dict = Depends(get_current_user)
):
    return LibroController.get_libros_paginados(page, limit)


@router.get("/{id_libro}", tags=["Libros"])
async def obtener_libro(
        id_libro: int,
        current_user: dict = Depends(get_current_user)
):
    return LibroController.obtener_libro(id_libro)


@router.post("/", tags=["Libros"], status_code=201)
async def crear_libro(
        libro: LibroCreate,
        _: bool = Depends(verificar_api_key)
):
    return LibroController.crear_libro_completo(
        titulo=libro.titulo,
        descripcion=libro.descripcion,
        fecha_publicacion=libro.fecha_publicacion,
        imagen_url=libro.imagen_url,
        autores=libro.autores,
        categorias=libro.categorias,
        ediciones=libro.ediciones
    )