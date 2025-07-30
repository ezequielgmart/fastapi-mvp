"""
the service is the business logic itself and should be called on the controllers. 
this is agnostic of the way that it's called

"""

# src/domains/authors/controller.py
from typing import List
from .repository import author_repository # Importa la instancia de tu servicio

from ..models.author import Author

class AuthorService:
    def get_all_authors(self) -> List[Author]:
        return author_repository.get_all()

# Instancia de tu controlador
author_service = AuthorService()