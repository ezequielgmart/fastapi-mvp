from pydantic import BaseModel, Field

# Este modelo es para las solicitudes (requests) POST y PUT.
# Contiene los campos que el cliente envía para crear o actualizar un recurso.
class GenreRequest(BaseModel):
    genre_name: str = Field(..., min_length=1)

# Este modelo representa el recurso completo que se almacena en la base de datos.
# Es el modelo que se usa para las respuestas (responses).
# Hereda de GenreRequest, por lo que incluye automáticamente el campo 'genre_name'.
class Genre(GenreRequest):
    genre_id: int
    
    class ConfigDict:
        # Esto es crucial para que Pydantic pueda mapear los datos
        # de un objeto de base de datos a tu modelo.
        from_attributes = True

# Este modelo es ideal para las solicitudes PUT/PATCH, donde un campo puede ser opcional.
class GenreUpdate(BaseModel):
    genre_name: str | None = None
