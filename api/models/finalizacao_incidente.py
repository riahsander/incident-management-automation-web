from pydantic import BaseModel


class FinalizacaoIncidente(BaseModel):
    hora_fim: str
    origem: str
    causa: str
    chamado: str
    escopo: str