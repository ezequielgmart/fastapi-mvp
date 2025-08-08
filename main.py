# src/main.py

from fastapi import FastAPI
from src.routes.v1.authors import router as authors_router
from src.routes.v1.books import router as books_router
from config.connect import CONFIG, create_db_pool

# src/main.py

from contextlib import asynccontextmanager

# Eventos de la aplicación para gestionar el pool de conexiones
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Función que se ejecuta al iniciar y al cerrar la aplicación para gestionar
    el pool de conexiones de la base de datos.
    """
    print("Creando pool de conexiones a la base de datos...")
    app.state.db_pool = await create_db_pool(CONFIG)
    print("Pool de conexiones creado con éxito.")
    yield
    print("Cerrando pool de conexiones...")
    if hasattr(app.state, 'db_pool') and app.state.db_pool:
        await app.state.db_pool.close()
    print("Pool de conexiones cerrado.")


# Creamos la instancia de FastAPI
app = FastAPI(
    title="API PyGem MVP",
    description="API de ejemplo usando PyGem y Pydantic.",
    version="0.1.0",
    lifespan=lifespan
)

# Incluimos el router de autores
app.include_router(
    authors_router,
    prefix="/authors",
    tags=["Authors"]
)

app.include_router(
    books_router,
    prefix="/books",
    tags=["Books"]
)