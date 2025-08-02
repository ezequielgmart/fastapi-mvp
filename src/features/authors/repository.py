"""

repo class interacts with the entity and provide the data to the service for the business logic
"""
from typing import List
from ..models.author import Author
from src.utils.exceptions import EXCEPTIONS
from config.db import AUTHORS

class AuthorRepositor:
    def get_all(self) -> List[Author]: # ¡Importante: tipa el retorno con tu modelo Pydantic!
        authors_data = AUTHORS
        # Pydantic puede validar y convertir directamente la lista de diccionarios
        # en una lista de objetos Author.
        return [Author(**data) for data in authors_data]
    
    def get_by_id(self, id:str): 

        authors_data = AUTHORS

        for author in authors_data:
            if id == author["author_id"]:
                # if we find the author, returns an instance of Author
                return Author(**author)
            
    
        return None
    
    def insert(self, author_obj:Author) -> Author: 
        if self.get_by_id(author_obj.author_id):
            # Podrías lanzar una excepción o manejarlo de otra forma si ya existe
            raise ValueError(f"{EXCEPTIONS["duplicated_author"]}")

        # convert hte pydantic obj on a dict before added on the AUTHORS collection 
        AUTHORS.append(author_obj.model_dump())

        return author_obj
     
            

# Instancia de tu servicio
author_repository = AuthorRepositor()