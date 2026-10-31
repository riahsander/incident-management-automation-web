from fastapi import APIRouter, HTTPException
from api.models.incidente import Incidente
from backend.services.incidente.executar_incidente import executar_incidente
from api.models.responses import IncidenteResponse
from backend.services.exceptions import AutomacaoException

router = APIRouter()

@router.post("/incidente", response_model=IncidenteResponse)
def criar_incidente(dados: Incidente):
    try:

        resultado = executar_incidente(dados.model_dump())

        return resultado
    except AutomacaoException as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )