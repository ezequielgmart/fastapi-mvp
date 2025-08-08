import uuid
from pydantic import BaseModel, Field
from datetime import date

class Book(BaseModel):
    book_id: str 
    title: str
    release_date: date # en el controlador la convertimos en una fecha

    class ConfigDict:
        from_attributes = True

# para usar en las penticiones HTTP        
class BookRequest(BaseModel):

    title:str
    release_date:str # la fecha llegara como un string

    class ConfigDict:

        from_attributes = True        