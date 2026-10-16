from fastapi import FastAPI
from datetime import datetime

APP = FastAPI()
TAREFAS=[]

#Estrutura da tarefa
"""
        "id": int,
        "titulo": str,
        "descricao": str,
        "concluida": boll,
        "criada_em": datetime()
"""

def criar_tarefa(titulo, descricao):
    return {
        "id": len(TAREFAS) + 1,
        "titulo": titulo,
        "descricao": descricao,
        "concluida": False,
        "criada_em": datetime.now()
    }


@APP.get("/")
async def index():
    return {"mensagem": "Ola Mundo"}


@APP.get("/tarefas")
async def listar_tarefas():
    return TAREFAS


@APP.post("/tarefas")
async def post_tarefa(titulo: str, descricao: str):
    tarefa_nova = criar_tarefa(titulo, descricao)
    TAREFAS.append(tarefa_nova)

    return {
        "mensagem": "Tarefa criada com sucesso",
        "tarefa": tarefa_nova
    }
