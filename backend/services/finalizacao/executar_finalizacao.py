from backend.services.incidente.salvar_incidente import salvar_incidente
from backend.services.qualitor.encerra_chamado import fecha_chamado
from backend.services.email.envio_email import fecha_email
from backend.services.exceptions import AutomacaoException
from backend.services.logger_config import logger

def Executar_Finalizacao(dados):
    try:
        logger.info("Salvando dados da finalização...")
        salvar_incidente(dados)

        logger.info("Encerrando chamado...")
        fecha_chamado()

        logger.info("Enviando e-mail de normalização...")
        fecha_email()

        return {
            "success": True,
            "message": "Incidente encerrado com sucesso",
        }
    except AutomacaoException:
        raise

    except Exception as erro:
        raise AutomacaoException(
            f"Erro inesperado durante a finalização: {erro}"
        ) from erro