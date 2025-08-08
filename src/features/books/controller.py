import uuid
from fastapi import HTTPException, status
from typing import List
from entities.book import Book, BookRequest
from .service import BookService
from datetime import datetime

class BookController:
    def __init__(self, service: BookService):
        self.service = service

    async def get_all(self) -> List[Book]:
        return await self.service.get_all_authors()

    async def get_by_id(self, book_id: str) -> Book:
        book = await self.service.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"id '{book_id}' not found."
            )
        return book

    async def create(self, request_data: BookRequest) -> Book:

        # recupero la data que viene desde el cliente api 
        # y genero un Author (model) valido para mi request. 
        book = {
            "book_id":str(uuid.uuid4()),
            "title":request_data.title,
            "release_date": datetime.strptime(request_data.release_date, '%Y-%m-%d').date()
        }
        
        new_item = await self.service.create_book(Book(**book))

        if not new_item:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unable to create a new Book"
            )
        return new_item
    
    async def update(self, book_id: str, book_data: BookRequest) -> Book:
        updated_item = await self.service.update_book(book_id, book_data)
        if not updated_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"id '{book_id}' not found."
            )
        return updated_item

    async def delete(self, book_id: str) -> Book:
        deleted_item = await self.service.delete_book(book_id)
        if not deleted_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"id '{book_id}' not found."
            )
        return deleted_item