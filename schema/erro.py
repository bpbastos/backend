from pydantic import BaseModel


class ErroSchema(BaseModel):
    """ Define como uma mensagem de eero será representada
    """
    erro: str