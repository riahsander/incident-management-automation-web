import json
import os
from backend.services.exceptions import AutomacaoException

from backend.services.path_utils import get_path


def salvar_incidente(dados: dict) -> None:
    """
    Salva os dados do incidente no arquivo info_incidente.json.

    Args:
        dados:
            Dicionário com as informações validadas do incidente.

    Raises:
        AutomacaoException:
            Quando os dados não podem ser gravados no arquivo.
    """
    try:
        file_path = get_path(
            os.path.join("data", "info_incidente.json")
        )

        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        with open(file_path, "w", encoding="utf-8") as arquivo:
            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )
    except Exception as erro:
        raise AutomacaoException("Erro ao salvar informações do incidente.") from erro