
from entities.book import Book
from pygem.main import GemRepository
from config.connect import DbPool
from entities.migrations import _books_gem

class BookRepository(GemRepository):
    def __init__(self, pool:DbPool):
        self.gem = _books_gem
        super().__init__(model=Book, gem=self.gem, pool=pool)

