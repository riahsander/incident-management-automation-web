from backend.services.incidente.salvar_incidente import salvar_incidente
from backend.services.qualitor.abertura_chamado import pega_chamado
from backend.services.gerar_screenshots.geral_function import gerar_screenshot
from backend.services.email.envio_email import enviar_email
from backend.services.exceptions import AutomacaoException
from backend.services.logger_config import logger
from backend.services.zerador_evidencias.zerar_evidencias import limpar_output

def executar_incidente(dados):
    try:
        logger.info("Apagando registros antigos...")
        limpar_output()

        logger.info("Salvando incidente...")
        salvar_incidente(dados)

        logger.info("Abrindo chamado...")
        chamado = pega_chamado()
        

        logger.info("Gerando evidências...")
        gerar_screenshot()

        logger.info("Enviando email...")
        enviar_email(chamado)

        return {
            "success": True,
            "message": "Incidente registrado com sucesso",
            "chamado": str(chamado)
        }
    except AutomacaoException:
        raise

    except Exception as erro:
        raise AutomacaoException(
            f"Erro inesperado durante o registro: {erro}"
        ) from erro