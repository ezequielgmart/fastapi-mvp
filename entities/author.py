import uuid
from pydantic import BaseModel, Field

class Author(BaseModel):
    # Usamos Field para definir un valor por defecto que se genera automáticamente
    author_id: str 
    first_name: str
    last_name: str
    nationality: str

    class ConfigDict:
        # Esto es útil si los datos provienen de un ORM o alguna otra fuente
        # que no devuelve diccionarios sino objetos con atributos.
        # En este caso no es estrictamente necesario ya que devuelves diccionarios,
        # pero es una buena práctica para futuras integraciones con DB.
        from_attributes = True
        
class AuthorRequest(BaseModel):

    first_name:str
    last_name:str
    nationality:str

    class ConfigDict:

        from_attributes = True        