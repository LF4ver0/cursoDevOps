"""Aplicação para o módulo de extensão DevOps"""

from datetime import datetime, timezone
from typing import Annotated, List
import os
import sys
import logging

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, Session, create_engine, select

from .modelo import Tarefa

LOGGER = logging.getLogger("aplicacao")
LOGGER.setLevel(logging.DEBUG)

saida_padrao = logging.StreamHandler()
arquivo = logging.FileHandler("aplicacao.log", encoding='utf-8')

formatador = logging.Formatter(
    "{name} | {levelname} | {asctime} | {filename}:{lineno} | {message}"
)

saida_padrao.setFormatter(formatador)
arquivo.setFormatter(formatador)

LOGGER.addHandler(saida_padrao)
LOGGER.addHandler(arquivo)

DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_ADDRESS = os.environ.get("DATABASE_ADDRESS")
DATABASE = os.environ.get("DATABASE")

if DATABASE_USERNAME is None:
    LOGGER.critical("DATABASE_USERNAME está faltando")
    sys.exit(1)

if DATABASE_PASSWORD is None:
    LOGGER.critical("DATABASE_PASSWORD está faltando")
    sys.exit(1)

if DATABASE_ADDRESS is None:
    LOGGER.critical("DATABASE_ADDRESS está faltando")
    sys.exit(1)

if DATABASE is None:
    LOGGER.critical("DATABASE está faltando")
    sys.exit(1)

DATABASE_URL = (
    "postgresql+psycopg://"
    f"{DATABASE_USERNAME}:{DATABASE_PASSWORD}"
    f"@{DATABASE_ADDRESS}:5432/{DATABASE}"
)

ENGINE = create_engine(DATABASE_URL)

def criar_sessao():
    """Função utilitária para criar sessão no banco de dados"""
    with Session(ENGINE) as s:
        yield s


SESSAO = Annotated[Session, Depends(criar_sessao)]


async def inicializacao(_: FastAPI):
    """Função para incialização da API e do banco de dados"""
    SQLModel.metadata.create_all(ENGINE)
    yield


APP = FastAPI(lifespan=inicializacao)
TAREFAS = []


# GET /tarefas: Lista todas as tarefas (somente id e titulo)
@APP.get("/tarefas")
async def tarefas(sessao: SESSAO) -> List[Tarefa]:
    """Rota para listar as tarefas."""

    lista_tarefas = sessao.exec(select(Tarefa).offset(0)).all()

    LOGGER.info("Usuário listou todas as tarefas")

    return lista_tarefas


# POST /tarefas: Cria tarefa
@APP.post("/tarefas", status_code=201)
async def post_tarefa(sessao: SESSAO, titulo: str, descricao: str = None):
    """Rota para criar uma tarefa."""
    data = datetime.now().astimezone(timezone.utc).replace(microsecond=0)
    tarefa_nova = Tarefa(
        titulo=titulo,
        descricao=descricao,
        data_criacao=data,
    )

    sessao.add(tarefa_nova)
    sessao.commit()
    sessao.refresh(tarefa_nova)

    LOGGER.info("Usuário criou a tarefa {tarefa_nova.get_id()}")
    LOGGER.debug(tarefa_nova)

    return {"mensagem": "OK"}


# GET /tarefas/{id_tarefa}: Visualizar tarefa específica
@APP.get("/tarefas/{id_tarefa}")
async def tarefa_especifica(sessao: SESSAO, id_tarefa: int) -> Tarefa:
    """Rota para visualizar uma tarefa específica"""
    # select * from tarefas where id == id_tarefa
    regra = select(Tarefa).where(Tarefa.id == id_tarefa)
    resultado = sessao.exec(regra).all()

    if resultado:
        LOGGER.info("Usuário visualizou a tarefa específica {Tarefa.id}")
        return resultado[0]

    LOGGER.info("Usuário tentou visualizar uma tarefa inexistente")
    return {"mensagem": "Tarefa não existe"}


# PUT /tarefas/{id}: Atualiza tarefa específica
@APP.put("/tarefas/{id_tarefa}")
async def concluir_tarefa(sessao: SESSAO, id_tarefa: int):
    """Rota para concluir uma tarefa."""

    # Atualizar a rota para suportar o SQLModel/Conexão com BD
    # Usar select para filtrar as tarefas com base no ID e se estiver concluída
    # Atualizar usando sessao.add, sessao.commit, sessao.refresh

    regra = select(Tarefa).where(Tarefa.id == id_tarefa)
    resultado = sessao.exec(regra).all()

    if not resultado:
        LOGGER.info("Usuário tentou concluir uma tarefa inexistente")
        return {"mensagem": "Tarefa não existe"}

    if resultado[0].concluida is True:
        LOGGER.info("Usuário tentou concluir uma tarefa ja concluida")
        return {"mensagem": "Tarefa já finalizada"}

    resultado[0].finalizar()

    sessao.add(resultado[0])
    sessao.commit()
    sessao.refresh(resultado[0])

    LOGGER.info("Usuário atualizou uma tarefa")

    return {"mensagem": "Tarefa atualizada"}


# DELETE /tarefas/{id_tarefa}: Exclui tarefa
@APP.delete("/tarefas/{id_tarefa}")
async def apagar_tarefa(sessao: SESSAO, id_tarefa: int):
    """Rota para apagar tarefa."""

    regra = select(Tarefa).where(Tarefa.id == id_tarefa)
    resultado = sessao.exec(regra).all()

    if not resultado:
        LOGGER.info("Usuário tentou excluir uma tarefa inexistente")
        return {"mensagem": "Tarefa não existe"}

    tarefa = resultado[0]

    sessao.delete(tarefa)
    sessao.commit()

    LOGGER.info("Usuário removeu uma tarefa")

    return {"mensagem": "Tarefa removida"}

@APP.exception_handler(404)
async def trata_404(_, __):
    """Captura de acesso a rota inexistente."""
    LOGGER.error("Página inexistente")
    return JSONResponse({"mensagem": "Página inexistente"})

@APP.get("/")
async def index():
    """Rota raíz."""
    return {"mensagem": "Olá, mundo!"}


# 1. Implementar uma rota chamada "/autor" que retorna
# um dicionário no formato {"mensagem": SEU NOME COMPLETO}
@APP.get("/autor")
async def autor():
    """Rota para retornar o autor da aplicação"""
    return {"mensagem": "Lucas Felipe"}
