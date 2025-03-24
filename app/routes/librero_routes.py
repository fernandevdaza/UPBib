from fastapi import APIRouter, HTTPException, Request, Header, Depends, Query
from app.controllers.librero_controller import LibreroController
from app.controllers.libro_controller import LibroController
from fastapi.responses import StreamingResponse
from app.utils.auth_middleware import get_current_user
import boto3
from PyPDF2 import PdfReader, PdfWriter
import io
import requests
from app.utils.s3_url import get_s3_url

router = APIRouter()
s3 = boto3.client('s3')
BUCKET_NAME = "upbib"

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


@router.get("/libros/", tags=["Libros"])
async def get_libros(current_user: dict = Depends(get_current_user)):
    return LibreroController.obtener_libros_librero(current_user['id'])


@router.get("/api/lector/{libro_id}")
async def leer_pdf(
        libro_id: int,
        pagina: int = Query(1, gt=0),
        usuario: dict = Depends(get_current_user)
):
    try:
        if not LibreroController.verificar_acceso(usuario['id'], libro_id):
            raise HTTPException(status_code=403, detail="Acceso denegado")

        libro_data = LibroController.obtener_metadatos(libro_id)
        if not libro_data:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        s3_key = libro_data['s3_key']
        pdf_url = get_s3_url(s3_key)

        response = requests.get(pdf_url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error al obtener PDF")

        with io.BytesIO(response.content) as pdf_data:
            reader = PdfReader(pdf_data)
            total_pages = len(reader.pages)

            # Calcular número máximo de "páginas virtuales" (cada una contiene 2 hojas)
            max_pagina = (total_pages + 1) // 2
            if pagina > max_pagina:
                raise HTTPException(422, "Página inválida")

            # Calcular rango de páginas reales
            start_page = (pagina - 1) * 2
            end_page = start_page + 2

            writer = PdfWriter()
            for page_num in range(start_page, min(end_page, total_pages)):
                writer.add_page(reader.pages[page_num])

            output_buffer = io.BytesIO()
            writer.write(output_buffer)
            output_buffer.seek(0)

            return StreamingResponse(
                output_buffer,
                media_type="application/pdf",
                headers={
                    "X-Total-Pages": str(total_pages),
                    "X-Total-Virtual-Pages": str(max_pagina),
                    "X-Current-Page": str(pagina),
                    "Access-Control-Expose-Headers": "X-Total-Pages, X-Total-Virtual-Pages, X-Current-Page",
                    "Content-Disposition": "inline; filename=document.pdf"
                }
            )

    except Exception as e:
        raise HTTPException(500, detail=str(e))