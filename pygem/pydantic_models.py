
from pydantic import BaseModel

class Field(BaseModel):
    is_primary_key:bool
    name:str
    type:str
    is_null:bool
    name:str

# 
