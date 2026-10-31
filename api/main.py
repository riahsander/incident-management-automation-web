import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.services.logger_config import configurar_logger
from backend.services.path_utils import get_output_path


# Configura o logger antes de importar os routers.
OUTPUT_DIR = get_output_path("output")
logger = configurar_logger(OUTPUT_DIR)


from api.routers.incidente import router as incidente_router
from api.routers.finalizacao import router as finalizacao_router


app = FastAPI(
    title="Automação Incidente Transacional",
    version="1.0.0",
    description=(
        "API responsável pela abertura e finalização "
        "de incidentes transacionais."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    logger.info("API da Automação Incidente Transacional iniciada.")


@app.on_event("shutdown")
def shutdown_event() -> None:
    logger.info("API da Automação Incidente Transacional encerrada.")


@app.get(
    "/",
    tags=["Status"],
    summary="Verifica o status da API",
)
def home():
    logger.debug("Consulta de status da API recebida.")

    return {
        "status": "online",
        "aplicacao": "Automação Incidente Transacional",
        "versao": app.version,
    }


app.include_router(incidente_router)
app.include_router(finalizacao_router)