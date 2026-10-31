"""
Captura de evidência dos gráficos transacionais.

O módulo utiliza Playwright para acessar o ambiente de gráficos
transacionais, localizar o gráfico correspondente à operadora e
armazenar sua captura como evidência do incidente.

A identificação do gráfico utilizado para cada parceiro é definida
externamente pelo mapeamento de operadoras.
"""

import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import re
from backend.services.path_utils import get_output_path 
from backend.services.logger_config import logger

load_dotenv()
transacional_graf = os.getenv("TRANSACIONAL_GRAF")
user = os.getenv("USER")
password = os.getenv("PASSWORD")


def print_grafico(operadora, pasta_saida):
    """
    Captura o gráfico transacional associado a uma operadora.

    A função autentica no ambiente de gráficos transacionais, localiza
    o componente correspondente à operadora e salva sua captura
    no diretório especificado.

    Args:
        operadora (str): Nome utilizado para localizar o gráfico.
        pasta_saida (str): Diretório onde a imagem será armazenada.

    Returns:
        None
    """
    logger.info("Capturando evidências dos Gráficos Transacionais...")
    try:
        """Gera o print do gráfico da operadora e salva no arquivo correto dentro da pasta de saída."""
        with sync_playwright() as p:
            browser = p.chromium.launch()

            page = browser.new_page()
            page.set_viewport_size({"width": 1920, "height": 1080})
            page.goto(transacional_graf)

            # Login
            page.fill("input[name='user']", user)
            page.fill("input[name='password']", password)
            page.click("button[type='submit']")


            # Fecha aba lateral
            botao_fechar_aba_lateral = page.locator("#dock-menu-button")
            botao_fechar_aba_lateral.click()
            page.wait_for_selector("section", state="visible", timeout=5000)
            page.wait_for_timeout(3000)

            try:
                # Localiza card do gráfico
                card_grafico = page.locator("section").filter(
                    has=page.locator("h2", has_text=re.compile(fr"^\s*{operadora}\s*$", re.IGNORECASE))
                )
                card_grafico.wait_for(state="visible", timeout=10000)
                card_grafico.scroll_into_view_if_needed()

                # Ajusta caminho de saída (arquivo completo, não pasta)
                pasta_saida = get_output_path(pasta_saida)  # garante que a pasta exista
                filename = f"{operadora}.png"
                full_path = os.path.join(pasta_saida, filename)

                # Garante que o caminho termina com .png
                if not full_path.lower().endswith(".png"):
                    full_path += ".png"

                # Salva o print diretamente no arquivo
                card_grafico.screenshot(path=full_path)
                logger.info(f"Arquivo salvo em: {full_path}")
                print(f"Arquivo salvo em: {full_path}")

            except Exception:
                logger.exception(f"ERRO ao tirar print do gráfico da operadora {operadora}")

            browser.close()
    except Exception: 
        logger.exception("Erro ao gerar screenshot dos gráficos transacionais. ")