from fastapi import APIRouter, HTTPException, Depends, Response, Request

from app.controllers.auth_controller import AuthController
from app.schemas.login import LoginRequest, RefreshRequest, RegisterRequest
from import_books import BookImporter

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest, response: Response):
    result = AuthController.login(request.email, request.password)
    if not result:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        secure=False,
        samesite="None",
        path="/auth/refresh-token"
    )

    return {
        "access_token": result["access_token"],
        "token_type": "bearer"
    }


@router.post("/register")
def register(request: RegisterRequest, response: Response):
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

    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        secure=False,
        samesite="lax",
        path="/auth/refresh-token"
    )

    return {
        "id_usuario": result["id_usuario"],
        "email": result["email"],
        "access_token": result["access_token"],
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(request: Request):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token missing")

    result = AuthController.logout(refresh_token)
    return result

@router.post("/refresh-token")
def refresh_token(request: RefreshRequest, response: Response):
    refresh_tok = request.cookies.get("refresh_token")
    if not refresh_tok:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    result = AuthController.refresh_token(request.refresh_token)

    if "error" in result:
        response.delete_cookie("refresh_token")
        raise HTTPException(status_code=401, detail=result["error"])

    return {"access_token": result["access_token"], "token_type": "bearer"}

@router.get("/load_books")
def load_books(request):
    importer = BookImporter(
        csv_path="app/books.csv",
        libros_dir="Libros",
        portadas_dir="Libros/Portadas",
        s3_bucket="upbib"
    )
    importer.run()

