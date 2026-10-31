import logging
import os
from logging.handlers import RotatingFileHandler


LOGGER_NAME = "AutomacaoIncidente"
LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | "
    "%(module)s | %(message)s"
)

logger = logging.getLogger(LOGGER_NAME)


def configurar_logger(output_dir: str) -> logging.Logger:
    """
    Configura o logger principal da aplicação.

    Cria a pasta de logs, configura a rotação automática e
    adiciona handlers de arquivo e console.

    Args:
        output_dir:
            Diretório base no qual a pasta `logs` será criada.

    Returns:
        Logger principal configurado.
    """

    if logger.handlers:
        return logger

    logs_dir = os.path.join(output_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    logs_file = os.path.join(logs_dir, "automacao.log")

    formatter = logging.Formatter(LOG_FORMAT)

    file_handler = RotatingFileHandler(
        filename=logs_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger