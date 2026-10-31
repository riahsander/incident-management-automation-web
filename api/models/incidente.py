from pydantic import BaseModel


class Incidente(BaseModel):
    parceiro: str
    tipo_transacao: str
    autorizador: str
    status: str
    indisponibilidade: str
    hora_inicio: str