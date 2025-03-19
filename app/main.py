from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from app.controllers.auth_controller import AuthController

app = FastAPI(
    title="UpBib - Biblioteca Digital UPB",
    description="Sistema de biblioteca digital para la Universidad Privada de Bolivia.",
    version="1.0.0"
)
AuthController.limpiar_tokens_expirados()

app.include_router(auth_router, prefix="/auth")
