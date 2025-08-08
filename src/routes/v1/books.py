from fastapi import APIRouter, Depends
from typing import List
from entities.book import Book, BookRequest
from src.features.books.dependencies import get_book_controller
from src.features.books.controller import BookController

router = APIRouter()

@router.get(
    "/",
    response_model=List[Book],
    summary="Obtener todos los libros",
    description="Retorna una lista de todos los libros disponibles en el sistema."
)
async def get_abooks(controller: BookController = Depends(get_book_controller)):
    return await controller.get_all()


@router.get(
    "/{book_id}",
    response_model=Book,  # Cambiado a un solo
    summary="Obtener un libro por ID",
    description="Retorna un libro específico basado en su ID."
)
async def get_book_by_id(
    book_id: str,  # ¡Ahora el parámetro de ruta está en la función!
    controller: BookController = Depends(get_book_controller)
):

    # El controller.get_by_id ahora recibe el parámetro book_id.
    return await controller.get_by_id(book_id)


@router.post(
    "/",
    response_model=Book,
    summary="Crear un nuevo libro",
    description="Crea un nuevo libro y lo retorna en caso de éxito."
)
async def create_book(
    book_data: BookRequest, 
    controller: BookController = Depends(get_book_controller)
):
    return await controller.create(book_data)


@router.put(
    "/{book_id}",
    response_model=Book,
    summary="Actualiza un libro existente",
    description="Actualiza un libro existente y lo retorna en caso de éxito."
)
async def update_book(
    book_id:str,
    book_data: BookRequest, 
    controller: BookController = Depends(get_book_controller)
):
    return await controller.update(book_id, book_data)


@router.delete(
    "/{book_id}",
    response_model=Book,
    summary="Elimina un libro existente",
    description="Elimina un libro existente"
)
async def delete_book(
    book_id:str,
    controller: BookController = Depends(get_book_controller)
):
    return await controller.delete(book_id)
