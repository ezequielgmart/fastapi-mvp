from fastapi import Depends
from config.connect import CONFIG
from config.connect import DbPool
from pygem.main import create_db_pool
from .repository import BookRepository
from .service import BookService
from .controller import BookController

# Este pool de conexiones se creará una sola vez para toda la aplicación.
async def get_db_pool():
    pool = await create_db_pool(CONFIG)
    try:
        yield pool
    finally:
        pool.close()

# Función que le dice a FastAPI cómo obtener una instancia de BookRepository
async def get_book_repository(pool: DbPool = Depends(get_db_pool)):
    return BookRepository(pool=pool)

# Función que le dice a FastAPI cómo obtener una instancia de bookService
async def get_book_service(repository: BookRepository = Depends(get_book_repository)):
    return BookService(repository=repository)

# Función que le dice a FastAPI cómo obtener una instancia de bookController
async def get_book_controller(service: BookService = Depends(get_book_service)):
    return BookController(service=service)
