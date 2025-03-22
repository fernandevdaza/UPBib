from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth_routes import router as auth_router
from app.controllers.auth_controller import AuthController
from app.routes.autor_routes import router as autor_router
from app.routes.libros_routes import router as libros_router
from app.routes.librero_routes import router as librero_router
from app.routes.categoria_routes import router as categoria_router

app = FastAPI(
    title="UpBib - Biblioteca Digital UPB",
    description="Sistema de biblioteca digital para la Universidad Privada de Bolivia.",
    version="1.0.0"
)
AuthController.limpiar_tokens_expirados()

app.include_router(auth_router, prefix="/auth")
app.include_router(autor_router, prefix="/autor")
app.include_router(libros_router, prefix="/libros")

app.include_router(librero_router, prefix="/librero")
app.include_router(categoria_router, prefix="/categoria")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Origen de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

