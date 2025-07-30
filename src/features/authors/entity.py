"""

the domain model or the object that represents the domain. 

"""
from pydantic import BaseModel

class Author(BaseModel):
    id: int
    name: str
    last_name: str
    nationality: str

    class Config:
        # Esto es útil si los datos provienen de un ORM o alguna otra fuente
        # que no devuelve diccionarios sino objetos con atributos.
        # En tu caso actual, no es estrictamente necesario ya que devuelves diccionarios,
        # pero es una buena práctica para futuras integraciones con DB.
        from_attributes = True
        
# note: this is only for mvp reason, here should be the author table describe as the GEM form  
class AuthorEntity:

    def get_all(self):

        authors = [
            {
                "id":1,
            "name":"Juan",
            "last_name":"Bosh",
            "nationality":"Dominican",
            },
            {
                
                "id":2,
            "name":"Miguel",
            "last_name":"de Cervates",
            "nationality":"Spain",
            },
            {
                
                "id":3,
            "name":"Adolf",
            "last_name":"Hitler",
            "nationality":"Austria",
            },]
        
        return authors