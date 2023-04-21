from datetime import datetime
from http.client import HTTPException
from typing import Optional,List
from pydantic import BaseModel, ValidationError, constr, validator

import re

from model import Session
from model.tarefa import Tarefa
from schema.categoria import CategoriaSchema


class _TarefaSchema(BaseModel):
    """
    " Schema responsável pela representação de uma Tarefa no sistema
    " A ideia era fazer todas as validações adicionais como minimo e maximo de caracteres,
    " além de unicidade no banco e validação de data.
    " Infelizmente não consegui implementar nenhuma validação extra. 
    " Pedi ajuda no discord - https://discordapp.com/channels/1040258631712653394/1040258632647983204/1097985257954869390
    " Porém não obtive ajuda, estou desistindo por conta do prazo de entrega e indo para uma solução mais simples
    " validando apenas os campos requeridos.
    """
    titulo:constr(min_length=3, max_length=40) = "Tarefa 1"
    detalhes:constr(min_length=3, max_length=4000) = "Detalhes da tarefa 1"
    data_limite:str = "04/05/2023"
    categoria_id:int = 1

    @validator('titulo', pre=True)
    def check_titulo(cls, value):
        s = Session();
        tarefa = s.query(Tarefa).filter(Tarefa.titulo == value).first()
        if tarefa: 
            raise ValueError("tarefa já existe no banco de dados")  
        return value 

    @validator('data_limite', pre=True)
    def check_data_limite(cls, value):
        data_re = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$'
        if not bool(re.fullmatch(data_re, value)):
            raise ValueError("data_limite inválida") 
        return value
    
class TarefaSchema(BaseModel):
    """
    " Schema responsável pela representação de uma Tarefa
    """    
    titulo:str = "Tarefa 1"
    detalhes:str = "Detalhes da tarefa 1"
    data_limite:str = "04/05/2023"
    categoria_id:int = 1   

class TarefaViewSchema(BaseModel):
    """
    " Schema responsável pela representação de uma Tarefa+Categoria
    """    
    id:int = 1
    titulo:str = "Tarefa 1"
    detalhes:str = "Detalhes da tarefa 1"
    data_limite:str = "04/05/2023"
    categoria:List[CategoriaSchema]     

class TarefaListSchema(BaseModel):
    """ Define como uma listagem de tarefas será representada.
    """
    tarefa:List[TarefaViewSchema]    

class TarefaPtrSchema(BaseModel):
    """ Define como representação dos parametros de busca da Tarefa
    """
    id:Optional[int] = 1
    titulo: Optional[str] = "Tarefa 1"

