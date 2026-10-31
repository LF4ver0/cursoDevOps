"""Aplicação para o módulo de extensão DevOps"""

from datetime import datetime, timezone
from typing import Annotated, List
import os
import sys
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, create_engine, select
from app.modelo import Tarefa

DB_USERNAME = os.environ.get("DATABASE_USERNAME")
DB_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DB_ADDRESS = os.environ.get("DATABASE_ADDRESS")
DB = os.environ.get("DATABASE")

if DB_USERNAME is None:
    print("DB_USERNAME está faltando")
    sys.exit(1)

if DB_PASSWORD is None:
    print("DB_PASSWORD está faltando")
    sys.exit(1)

if DB_ADDRESS is None:
    print("DB_ADDRESS está faltando")
    sys.exit(1)

if DB is None:
    print("DB está faltando")
    sys.exit(1)

ENGINE = create_engine(
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_ADDRESS}:3306/{DB}"
)


def criar_sessao():
    """Função que cria sessão do BD"""
    with Session(ENGINE) as s:
        yield s


SESSAO = Annotated[Session, Depends(criar_sessao)]


async def inicializacao(_api: FastAPI):
    """Cria Instancia do BD"""
    SQLModel.metadata.create_all(ENGINE)
    yield


APP = FastAPI(lifespan=inicializacao)
TAREFAS = []


# GET /tarefas: Lista todas as tarefas (somente id e titulo)
@APP.get("/tarefas")
async def tarefas(sessao: SESSAO) -> List[Tarefa]:
    """Rota para listar as tarefas."""

    lista_tarefas = sessao.exec(select(Tarefa).offset(0)).all()

    return lista_tarefas


# POST /tarefas: Cria tarefa
@APP.post("/tarefas", status_code=201)
async def post_tarefa(sessao: SESSAO, titulo: str, descricao: str = None):
    """Rota para criar uma tarefa."""
    tarefa_nova = Tarefa(
        titulo=titulo,
        descricao=descricao,
        data_criacao=datetime.now().astimezone(timezone.utc),
    )

    sessao.add(tarefa_nova)
    sessao.commit()
    sessao.refresh(tarefa_nova)

    return {"mensagem": "OK"}


# GET /tarefas/{id_tarefa}: Visualizar tarefa específica
@APP.get("/tarefas/{id_tarefa}")
async def tarefa_especifica(sessao: SESSAO, id_tarefa: int) -> Tarefa:
    """Rota para visualizar uma tarefa específica"""
    # 1. Selecionar a tarefa de ID recebido como parâmetro
    # 2. Retornar todos os dados da tarefa
    # 3. Caso a tarefa não exista, você tem que mostrar que a tarefa não existe

    regra = select(Tarefa).where(Tarefa.id == id_tarefa)
    resultado = sessao.exec(regra).all()

    if resultado:
        return resultado[0]

    return {"mensagem": "Tarefa não existe"}


# PUT /tarefas/{id}: Atualiza tarefa específica
@APP.put("/tarefas/{id_tarefa}")
async def concluir_tarefa(sessao: SESSAO, id_tarefa: int):
    """Rota para concluir uma tarefa."""
    # 1. Selecionar a tarefa de ID recebido como parâmetro
    # 2. Marcar a tarefa como concluída
    # 3. Você deve armazenar o horário de conclusão da tarefa
    # 4. Caso a tarefa não exista, você tem que mostrar que a tarefa não existe

    regra = select(Tarefa).where(Tarefa.id == id_tarefa and Tarefa.concluida is False)
    resultado = sessao.exec(regra).all()

    if not resultado:
        return {"mensagem": "Tarefa não existe"}

    if resultado[0].concluida is True:
        return {"mensagem": "Tarefa já finalizada"}

    resultado[0].finalizar()
    sessao.add(resultado[0])
    sessao.commit()
    sessao.refresh(resultado[0])

    return {"mensagem": "Tarefa atualizada"}

    # try:
    #     _ = requests.post(
    #         f"http://localhost:8000/notificar?id={resultado.id}&titulo={resultado.titulo}",
    #         timeout=1,
    #     )
    # except RequestConnectionError as e:
    #     print(e)


# DELETE /tarefas/{id_tarefa}: Exclui tarefa
@APP.delete("/tarefas/{id_tarefa}")
async def apagar_tarefa(sessao: SESSAO, id_tarefa: int):
    """Rota para apagar tarefa."""
    # 1. Selecionar a tarefa de ID recebido como parâmetro
    # 2. Remover tarefa da lista de tarefas
    # 3. Caso a tarefa não exista, você tem que mostrar que a tarefa não existe

    regra = select(Tarefa).where(Tarefa.id == id_tarefa)
    resultado = sessao.exec(regra).all()

    if not resultado:
        return {"mensagem": "Tarefa não existe"}

    sessao.delete(resultado[0])
    sessao.commit()

    return {"mensagem": "Tarefa apagada"}


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
