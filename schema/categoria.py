from typing import List
from pydantic import BaseModel

class CategoriaSchema(BaseModel):
    id: int
    nome:str

class CategoriaListSchema(BaseModel):
    """ Define como uma listagem de categorias será representada.
    """
    categorias:List[CategoriaSchema]  
