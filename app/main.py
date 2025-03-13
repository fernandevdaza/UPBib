from fastapi import FastAPI

app = FastAPI(
    title="UpBib - Biblioteca Digital UPB",
    description="Sistema de biblioteca digital para la Universidad Privada de Bolivia.",
    version="1.0.0"
)

@app.get("/hello")
def hello_world():
    return {"message": "Hello, World!"}
