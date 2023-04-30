from typing import Optional,List
from pydantic import BaseModel, constr, validator

import re

from model import Session
from model.categoria import Categoria
from model.tarefa import Tarefa
from schema.categoria import CategoriaSchema

class TarefaSchema(BaseModel):
    """
    " Schema responsável pela representação de uma Tarefa no sistema
    " A ideia era fazer todas as validações adicionais como minimo e maximo de caracteres,
    " além de unicidade no banco e validação de data.
    " Não consegui implementar o tratamento da maneira que gostaria, pois não é possível capturar via try-catch 
    " quando o 422 acontece, dessa forma não foi possivel normalizar as msgs de erro.
    " O tratamento ficou do lado do cliente via JavaScript. 
    " Discord - https://discordapp.com/channels/1040258631712653394/1040258632647983204/1097985257954869390
    """
    titulo:constr(min_length=3, max_length=40) = "Tarefa 1"
    detalhes:constr(min_length=3, max_length=255) = "Detalhes da tarefa 1"
    data_limite:str = "04/05/2023"
    categoria_id:int = 1

    #Mensagens de erro personalizadas
    class Config:
        validate_assignment = True
        error_msg_templates = {
            "value_error.any_str.min_length": "mínimo de {limit_value} caracteres não alcançado",
            "value_error.any_str.max_length": "máximo de {limit_value} caracteres exedido",
            "type_error.integer": "não é um inteiro válido"
        }

    """
    " Valida se o campo titulo já existe no banco de dados
    """
    @validator('titulo')
    def check_titulo(cls, value):
        s = Session();
        tarefa = s.query(Tarefa).filter(Tarefa.titulo == value).first()
        if tarefa: 
            raise ValueError("já existe no banco de dados")  
        return value 
    
    """
    " Valida se a categoria é válida
    """
    @validator('categoria_id')
    def check_categoria(cls, value):
        s = Session();
        categoria = s.query(Categoria).filter(Categoria.id == value).first()
        if not categoria: 
            raise ValueError("inválida")  
        return value    
    
    """
    " Valida se o data_limite está em um formato válido
    """    
    @validator('data_limite')
    def check_data_limite(cls, value):
        data_re = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$'
        if not bool(re.fullmatch(data_re, value)):
            raise ValueError("inválida") 
        return value
    
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
    id:Optional[int] = None
    titulo: Optional[str] = None
    categoria_id: Optional[str] = None

