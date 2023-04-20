from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model.base import Base

class Tarefa(Base):
    __tablename__ = 'tarefa'

    id = Column("pk_tarefa", Integer, primary_key=True)
    titulo = Column(String(140), unique=True)
    detalhes = Column(String(4000))
    data_limite = Column(DateTime, default=datetime.now())

    # Definição do relacionamento um para muitos entre a tarefa e a categoria.
    categoria_id = Column("fk_categoria", Integer, ForeignKey("categoria.pk_categoria"), unique=False, nullable=False)
    categoria = relationship("Categoria", back_populates="tarefas")

    def __init__(self, titulo:str, detalhes:str, 
                 data_limite:Union[DateTime, None] = None,
                 categoria_id:int = 1):
        """
        Cria uma Tarefa
        Arguments:
            titulo: título da tarefa.
            detalhes: descrição detalhada da tarefa
            data_limite: data limite da tarefa
        """
        self.titulo = titulo
        self.detalhes = detalhes
        self.data_limite = data_limite
        self.categoria_id = categoria_id

        # se não for informada, será a data exata da inserção no banco
        if data_limite:
            self.data_limite = data_limite

