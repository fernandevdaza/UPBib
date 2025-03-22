from fastapi import APIRouter, HTTPException, Depends
from app.controllers.auth_controller import AuthController
from app.schemas.login import LoginRequest, RefreshRequest, RegisterRequest
from import_books import BookImporter

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest):
    result = AuthController.login(request.email, request.password)
    if not result:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {
        "access_token": result["access_token"],
        "refresh_token": result["refresh_token"],
        "token_type": "bearer"
    }


@router.post("/register")
def register(request: RegisterRequest):
    result = AuthController.register(
        request.nombre,
        request.apellido,
        request.fecha_nacimiento,
        request.email,
        request.password,
        request.codigo_upb
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result

@router.post("/logout")
def logout(request: RefreshRequest):
    result = AuthController.logout(request.refresh_token)
    return result

@router.post("/refresh-token")
def refresh_token(request: RefreshRequest):
    result = AuthController.refresh_token(request.refresh_token)
    return result

@router.get("/load_books")
def load_books(request):
    importer = BookImporter(
        csv_path="app/books.csv",
        libros_dir="Libros",
        portadas_dir="Libros/Portadas",
        s3_bucket="upbib"
    )
    importer.run()

