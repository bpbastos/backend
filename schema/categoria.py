from typing import List
from pydantic import BaseModel

class CategoriaSchema(BaseModel):
    """ Define como uma categoria será representada.
    """    
    id: int
    nome:str

class CategoriaListSchema(BaseModel):
    """ Define como uma listagem de categorias será representada.
    """
    categorias:List[CategoriaSchema]  
