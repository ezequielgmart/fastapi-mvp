"""
the service is the business logic itself and should be called on the controllers. 
this is agnostic of the way that it's called

"""

from typing import List, Optional
from entities.author import Author, AuthorRequest
from .repository import AuthorRepository

class AuthorService:
    def __init__(self, repository: AuthorRepository):
        self.repository = repository

    async def get_all_authors(self) -> List[Author]:
        return await self.repository.get_all()

    async def get_by_id(self, author_id: str) -> Optional[Author]:
        return await self.repository.get_by_id(author_id)

    async def create_author(self, new_author: Author) -> Optional[Author]:
        return await self.repository.create(new_author)
    
    async def update_author(self, author_id: str, author_data: AuthorRequest) -> Optional[Author]:
        existing_author = await self.repository.get_by_id(author_id)
        if not existing_author:
            return None
        
        updated_data = existing_author.model_copy(update=author_data.model_dump(exclude_unset=True))
        return await self.repository.update(author_id, updated_data)

    async def delete_author(self, author_id: str) -> Optional[Author]:
        return await self.repository.delete(author_id)
