
import os
from backend.services.logger_config import logger

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

def get_path(relative_path: str) -> str:

    try:
        return os.path.join(BASE_DIR, relative_path)
    except Exception:
        logger.exception("Erro ao resolver caminho do recurso.")
        raise


def get_output_path(relative_path):

    try:
        full_path = os.path.join(BASE_DIR,relative_path)

        os.makedirs(full_path,exist_ok=True)

        return full_path
    except Exception:
        logger.exception("Erro ao resolver diretório de saída.")
        raise