# UpBib - Biblioteca Digital para la UPB

**UpBib** es una biblioteca digital para la Universidad Privada de Bolivia (UPB) que permite a los estudiantes acceder a libros digitales sin permitir descargas ilegales. El sistema gestiona préstamos con acceso temporal a los libros, revocando automáticamente el acceso cuando expire el préstamo. Además, permite a los usuarios visualizar los libros en línea y gestionar su librero personal.

## Arquitectura

El proyecto sigue una arquitectura modular basada en **FastAPI** y **Docker**. Se utiliza **MySQL** como base de datos y **JWT** para la autenticación de usuarios. La aplicación se ejecuta en un entorno de contenedores Docker, lo que facilita el despliegue y la gestión de las dependencias.

### Estructura de Carpetas

```plaintext
upbib_project/
│
├── app/                          # Contendrá la aplicación FastAPI
│   ├── __init__.py
│   ├── main.py                   # Punto de entrada de la aplicación (FastAPI)
│   ├── config.py                 # Configuración general (conexión DB, claves secretas)
│   ├── models/                   # Modelos de la base de datos (SQLAlchemy, si es necesario)
│   │   └── libro.py              # Modelo para los libros
│   │   └── miembro.py            # Modelo para los miembros/usuarios
│   │   └── prestamo.py           # Modelo para los préstamos, si lo agregas
│   │   └── object_storage.py     # Modelo para vincular los archivos con los libros
│   ├── schemas/                  # Pydantic models (validación de datos)
│   │   └── libro.py              # Esquema Pydantic para los libros
│   │   └── miembro.py            # Esquema Pydantic para los miembros
│   │   └── auth.py               # Esquema para login, JWT, etc.
│   ├── services/                 # Lógica de negocio (funciones que gestionan la base de datos)
│   │   └── libro_service.py      # Servicios para manipular libros
│   │   └── auth_service.py       # Lógica para autenticación y generación de JWT
│   │   └── miembro_service.py    # Lógica para manejar miembros
│   ├── routes/                   # Rutas de la API
│   │   └── libro_routes.py       # Rutas para libros
│   │   └── auth_routes.py        # Rutas de autenticación (login, registro)
│   │   └── miembro_routes.py     # Rutas para gestión de miembros
│   ├── dependencies/             # Dependencias compartidas (e.g., verificación de JWT)
│   │   └── jwt.py                # Verificación de JWT y dependencias
│   └── utils/                    # Funciones y utilidades generales
│       └── hashing.py            # Función para hashing de contraseñas
│       └── db.py                 # Conexión a la base de datos
│
├── docker/                       # Contendrá los archivos Docker relacionados
│   ├── Dockerfile                # Dockerfile para la app FastAPI
│   ├── docker-compose.yml        # Docker Compose para orquestar los contenedores (app y db)
│   ├── .dockerignore             # Archivos a excluir en el contenedor Docker
│
├── .env                          # Variables de entorno (claves secretas, conexión DB, etc.)
├── Pipfile                       # Gestión de dependencias con pipenv
├── Pipfile.lock                  # Archivo bloqueado de dependencias con pipenv
├── requirements.txt              # Si prefieres usar requirements.txt, este archivo es útil
├── alembic.ini                   # Configuración de migraciones con Alembic (si lo usas)
├── README.md                     # Descripción del proyecto y su configuración
└── tests/                        # Carpeta de pruebas
    ├── __init__.py
    ├── test_auth.py              # Pruebas para la autenticación
    ├── test_libros.py            # Pruebas para los libros
    ├── test_members.py           # Pruebas para los miembros
```

---

## Requisitos

Asegúrate de tener **Docker** y **Docker Compose** instalados en tu máquina.

- Python 3.12.7+
- Docker
- Docker Compose

## Configuración del Proyecto

Sigue estos pasos para hacer el setup y correr el proyecto en tu máquina local:

### 1. Clona el repositorio

```bash
git clone https://github.com/tu-usuario/upbib.git
cd upbib
```

### 2. Instalar dependencias

#### Usando `pipenv`:

Este proyecto usa `pipenv` para gestionar las dependencias. Si no lo tienes instalado, puedes hacerlo ejecutando:

```bash
pip install pipenv
```

Ahora instala las dependencias con:

```bash
pipenv install
```

Para activar el entorno virtual:

```bash
pipenv shell
```

### 3. Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto y agrega las siguientes variables:

```plaintext
DATABASE_URL=mysql://root:root@db:3306/upbib
JWT_SECRET_KEY=tu_clave_secreta
```

- **`DATABASE_URL`**: URL de conexión a la base de datos MySQL. En este caso, Docker usará un contenedor con nombre `db`.
- **`JWT_SECRET_KEY`**: Clave secreta para firmar los tokens JWT.

### 4. Construir y Correr los Contenedores con Docker

El proyecto utiliza **Docker** y **Docker Compose** para manejar los contenedores. Para construir y correr los contenedores, usa:

```bash
docker-compose up --build
```

Esto iniciará la aplicación FastAPI y la base de datos MySQL en contenedores Docker. La aplicación estará disponible en `http://localhost:8000`.

### 5. Verificar el Funcionamiento de la API

Puedes probar la API usando **Swagger** (viene integrado con FastAPI) en `http://localhost:8000/docs`.

También puedes probar las rutas usando **Postman** o cualquier herramienta similar, enviando solicitudes con los JWT generados.

---

## Pruebas

Para ejecutar las pruebas, puedes usar **pytest**. Asegúrate de que todas las dependencias estén instaladas y luego ejecuta:

```bash
pytest
```

Las pruebas están ubicadas en la carpeta `tests/`.

---

## Estructura de la API

### Rutas Principales

1. **Autenticación**
   - **POST /auth/login**: Inicia sesión con email y contraseña. Devuelve un JWT.
   - **POST /auth/register**: Registra un nuevo usuario.

2. **Libros**
   - **GET /libros**: Obtiene todos los libros disponibles.
   - **GET /libros/{isbn}**: Obtiene los detalles de un libro específico.
   - **POST /libros**: Crea un nuevo libro (solo para administradores).

3. **Miembros**
   - **GET /miembros/me**: Obtiene los datos del miembro autenticado.

---

## Contribución

Si quieres contribuir al proyecto, por favor, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tus cambios (`git checkout -b feature-nueva-funcionalidad`).
3. Haz un commit con tus cambios (`git commit -am 'Añadir nueva funcionalidad'`).
4. Sube los cambios (`git push origin feature-nueva-funcionalidad`).
5. Abre un pull request con una descripción de lo que has hecho.

---

## Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo `LICENSE` para más detalles.
