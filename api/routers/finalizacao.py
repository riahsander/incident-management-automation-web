from fastapi import APIRouter, HTTPException
from api.models.finalizacao_incidente import FinalizacaoIncidente
from backend.services.finalizacao.executar_finalizacao import Executar_Finalizacao
from api.models.responses import IncidenteResponse
from backend.services.exceptions import AutomacaoException



router = APIRouter()

@router.post("/finalizar-incidente", response_model=IncidenteResponse)
def finalizar_incidente(dados: FinalizacaoIncidente):
    try:
        resultado = Executar_Finalizacao(dados.model_dump())
        return resultado
    except AutomacaoException as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )