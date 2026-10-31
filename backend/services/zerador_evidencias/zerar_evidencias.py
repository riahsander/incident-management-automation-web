import os
import shutil

from backend.services.path_utils import get_path
from backend.services.logger_config import logger

PASTAS_DE_EVIDENCIAS = (
    "printGraf",
    "printOP",
    "printOP_detalhado",
)


def limpar_output() -> None:
    """
    Remove as evidências geradas por execuções anteriores.

    A pasta `output/logs` não é removida, pois o arquivo de log
    permanece aberto durante a execução da aplicação.
    """

    output_dir = get_path("output")

    for nome_pasta in PASTAS_DE_EVIDENCIAS:
        caminho = os.path.join(output_dir, nome_pasta)

        try:
            if os.path.exists(caminho):
                shutil.rmtree(caminho)
                logger.info("Evidências antigas removidas: %s", caminho, )

                os.makedirs(caminho, exist_ok=True)
        except OSError:
            logger.exception("Erro ao limpar a pasta de evidências: %s", caminho, )
            raise