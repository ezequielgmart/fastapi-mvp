from typing import List, Optional
from entities.book import Book,BookRequest
from .repository import BookRepository

class BookService:

    def __init__(self, repository: BookRepository):
        self.repository = repository

        
    async def get_all_authors(self) -> List[Book]:
        return await self.repository.get_all()

    async def get_by_id(self, book_id: str) -> Optional[Book]:
        return await self.repository.get_by_id(book_id)

    async def create_book(self, new_book: Book) -> Optional[Book]:
        return await self.repository.create(new_book)
    
    async def update_book(self, book_id: str, book_data: BookRequest) -> Optional[Book]:
        existing_book = await self.repository.get_by_id(book_id)
        if not existing_book:
            return None
        
        updated_data = existing_book.model_copy(update=book_data.model_dump(exclude_unset=True))
        return await self.repository.update(book_id, updated_data)

    async def delete_book(self, book_id: str) -> Optional[Book]:
        return await self.repository.delete(book_id)
