from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from  model import Base

class Categoria(Base):
    __tablename__ = 'categoria'

    id = Column("pk_categoria", Integer, primary_key=True)
    nome = Column(String(140), unique=True)

    # Definição do relacionamento um para muitos entre a categoria e tarefa.    
    tarefas = relationship("Tarefa", back_populates="categoria", lazy="dynamic")

    def __init__(self, nome:str):
        """
        Cria uma Categoria
        Arguments:
            nome: o nome da categoria.
        """
        self.nome = nome
        