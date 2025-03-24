from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse

from app.controllers.auth_controller import AuthController
from app.schemas.login import LoginRequest, RefreshRequest, RegisterRequest, LogoutRequest
from import_books import BookImporter

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest):
    result = AuthController.login(request.email, request.password)
    if not result:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    response = JSONResponse( {
        "access_token": result["access_token"],
        "token_type": "bearer"
    }, headers={
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Origin": "*",
    })
    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        max_age=7 * 24 * 60 * 60,
        path="/auth/refresh-token"
    )

    return response


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

    response = JSONResponse( {
        "id_usuario": result["id_usuario"],
        "email": result["email"],
        "access_token": result["access_token"],
        "token_type": "bearer"
    }, headers={
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Origin": "*",
    })


    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        max_age=7 * 24 * 60 * 60,
        path="/auth/refresh-token"
    )

    return response


@router.post("/logout")
async def logout(request: LogoutRequest):

    if not request.refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token missing")

    result = AuthController.logout(request.refresh_token)
    return result

@router.post("/refresh-token")
def refresh_token(request: RefreshRequest):
    refresh_tok = request.cookies.get("refresh_token")
    if not refresh_tok:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    result = AuthController.refresh_token(request.refresh_token)

    response = JSONResponse( {"access_token": result["access_token"], "token_type": "bearer"})

    if "error" in result:
        response.delete_cookie("refresh_token")
        raise HTTPException(status_code=401, detail=result["error"])

    return response

@router.get("/load_books")
def load_books(request):
    importer = BookImporter(
        csv_path="app/books.csv",
        libros_dir="Libros",
        portadas_dir="Libros/Portadas",
        s3_bucket="upbib"
    )
    importer.run()

