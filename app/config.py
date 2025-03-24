import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "mi_clave_secreta")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql://root:root@db:3306/upbib")

    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"


settings = Settings()
