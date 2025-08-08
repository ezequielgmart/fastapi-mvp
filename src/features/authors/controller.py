# src/features/authors/controller.py
import uuid
from fastapi import HTTPException, status
from typing import List
from entities.author import Author, AuthorRequest
from .service import AuthorService

class AuthorController:
    def __init__(self, service: AuthorService):
        self.service = service

    async def get_all(self) -> List[Author]:
        return await self.service.get_all_authors()

    async def get_by_id(self, author_id: str) -> Author:
        print(author_id)
        author = await self.service.get_by_id(author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with id '{author_id}' not found."
            )
        return author

    async def create(self, request_data: AuthorRequest) -> Author:

        # recupero la data que viene desde el cliente api 
        # y genero un Author (model) valido para mi request. 
        author = {
            "author_id":str(uuid.uuid4()),
            "first_name":request_data.first_name,
            "last_name":request_data.last_name,
            "nationality":request_data.nationality,
        }
        
        new_author = await self.service.create_author(Author(**author))

        if not new_author:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unable to create a new Author"
            )
        return new_author
    
    async def update(self, author_id: str, author_data: AuthorRequest) -> Author:
        updated_author = await self.service.update_author(author_id, author_data)
        if not updated_author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with id '{author_id}' not found."
            )
        return updated_author

    async def delete(self, author_id: str) -> Author:
        deleted_author = await self.service.delete_author(author_id)
        if not deleted_author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with id '{author_id}' not found."
            )
        return deleted_author