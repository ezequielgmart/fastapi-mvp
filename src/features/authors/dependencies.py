# src/features/authors/dependencies.py
from fastapi import Depends
# from config.db import CONFIG
from config.connect import DbPool, CONFIG
from pygem.main import create_db_pool
from .repository import AuthorRepository
from .service import AuthorService
from .controller import AuthorController

# Este pool de conexiones se creará una sola vez para toda la aplicación.
async def get_db_pool():
    pool = await create_db_pool(CONFIG)
    try:
        yield pool
    finally:
        pool.close()

# Función que le dice a FastAPI cómo obtener una instancia de AuthorRepository
async def get_author_repository(pool: DbPool = Depends(get_db_pool)):
    return AuthorRepository(pool=pool)

# Función que le dice a FastAPI cómo obtener una instancia de AuthorService
async def get_author_service(repository: AuthorRepository = Depends(get_author_repository)):
    return AuthorService(repository=repository)

# Función que le dice a FastAPI cómo obtener una instancia de AuthorController
async def get_author_controller(service: AuthorService = Depends(get_author_service)):
    return AuthorController(service=service)

"""

    @function:
    @params:
    @return:

"""