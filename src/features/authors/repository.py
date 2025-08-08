from entities.author import Author
from pygem.main import GemRepository
from config.connect import DbPool
from entities.migrations import _authors_gem

class AuthorRepository(GemRepository):
    def __init__(self, pool: DbPool):
        self.gem = _authors_gem
        super().__init__(model=Author, gem=self.gem, pool=pool)
 
