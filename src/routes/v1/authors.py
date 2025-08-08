from fastapi import APIRouter, Depends
from typing import List
from entities.author import Author, AuthorRequest
from src.features.authors.dependencies import get_author_controller
from src.features.authors.controller import AuthorController

router = APIRouter()

@router.get(
    "/",
    response_model=List[Author],
    summary="Obtener todos los autores",
    description="Retorna una lista de todos los autores disponibles en el sistema."
)
async def get_authors(controller: AuthorController = Depends(get_author_controller)):
    return await controller.get_all()


@router.get(
    "/{author_id}",
    response_model=Author,  # Cambiado a un solo Author
    summary="Obtener un autor por ID",
    description="Retorna un autor específico basado en su ID."
)
async def get_author_by_id(
    author_id: str,  # ¡Ahora el parámetro de ruta está en la función!
    controller: AuthorController = Depends(get_author_controller)
):
    # La función debe llamarse get_author_by_id para mayor claridad.
    # El controller.get_by_id ahora recibe el parámetro author_id.
    return await controller.get_by_id(author_id)


@router.post(
    "/",
    response_model=Author,
    summary="Crear un nuevo autor",
    description="Crea un nuevo autor y lo retorna en caso de éxito."
)
async def create_author(
    author_data: AuthorRequest, 
    controller: AuthorController = Depends(get_author_controller)
):
    return await controller.create(author_data)


@router.put(
    "/{author_id}",
    response_model=Author,
    summary="Actualiza un autor existente",
    description="Actualiza un autor existente y lo retorna en caso de éxito."
)
async def update_author(
    author_id:str,
    author_data: AuthorRequest, 
    controller: AuthorController = Depends(get_author_controller)
):
    return await controller.update(author_id, author_data)


@router.delete(
    "/{author_id}",
    response_model=Author,
    summary="Elimina un autor existente",
    description="Elimina un autor existente"
)
async def delete_author(
    author_id:str,
    controller: AuthorController = Depends(get_author_controller)
):
    return await controller.delete(author_id)
