from pydantic import BaseModel

class Author(BaseModel):
    id: str
    title: str
    release_date: str
    

    class ConfigDict:
        # Esto es útil si los datos provienen de un ORM o alguna otra fuente
        # que no devuelve diccionarios sino objetos con atributos.
        # En tu caso actual, no es estrictamente necesario ya que devuelves diccionarios,
        # pero es una buena práctica para futuras integraciones con DB.
        from_attributes = True
        