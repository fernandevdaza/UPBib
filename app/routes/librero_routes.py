from fastapi import APIRouter, HTTPException, Request, Header, Depends, Query
from app.controllers.librero_controller import LibreroController
from app.controllers.libro_controller import LibroController
from fastapi.responses import StreamingResponse
from app.utils.auth_middleware import get_current_user
import boto3
from PyPDF2 import PdfReader, PdfWriter
import io

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
        try:
            response = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
        except s3.exceptions.NoSuchKey:
            raise HTTPException(404, "Archivo no encontrado en S3")
        except Exception as s3_error:
            raise HTTPException(500, f"Error de S3: {str(s3_error)}")

        with io.BytesIO(response['Body'].read()) as pdf_data:
            reader = PdfReader(pdf_data)
            total_pages = len(reader.pages)

            if total_pages == 0:
                raise HTTPException(422, "El archivo PDF está vacío")

            pages_per_request = 2
            start_page = (pagina - 1) * pages_per_request
            end_page = start_page + pages_per_request

            if start_page >= total_pages:
                raise HTTPException(422, "Número de página inválido")

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
                    "X-Current-Page": str(pagina),
                    "Content-Disposition": "inline; filename=document.pdf"
                }
            )

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(500, "Error procesando el documento")