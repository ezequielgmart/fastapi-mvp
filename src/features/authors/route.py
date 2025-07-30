# src/domains/authors/route.py
from fastapi import APIRouter
from typing import List
from .service import author_service # Importa la instancia de tu controlador
from .entity import Author # Importa tu modelo Pydantic para response_model

router = APIRouter()

@router.get(
    "/",
    response_model=List[Author], # ¡Aquí le decimos a FastAPI qué tipo de datos esperamos como respuesta!
    summary="Obtener todos los autores",
    description="Retorna una lista de todos los autores disponibles en el sistema."
)
async def get_all_authors_route():
    """
    Ruta para obtener todos los autores.
    """
    return author_service.get_all_authors()