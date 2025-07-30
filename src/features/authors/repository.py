"""

repo class interacts with the entity and provide the data to the service for the business logic
"""
from typing import List
from ..models.author import Author

class AuthorRepositor:
    def get_all(self) -> List[Author]: # ¡Importante: tipa el retorno con tu modelo Pydantic!
        authors_data = [
            {
                "id": 1,
                "name": "Juan",
                "last_name": "Bosh",
                "nationality": "Dominican",
            },
            {
                "id": 2,
                "name": "Miguel",
                "last_name": "de Cervates",
                "nationality": "Spain",
            },
            {
                "id": 3,
                "name": "Adolf",
                "last_name": "Hitler",
                "nationality": "Austria",
            },
        ]
        # Pydantic puede validar y convertir directamente la lista de diccionarios
        # en una lista de objetos Author.
        return [Author(**data) for data in authors_data]

# Instancia de tu servicio
author_repository = AuthorRepositor()