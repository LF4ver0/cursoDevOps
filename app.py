from fastapi import FastAPI
from datetime import datetime
import requests

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


@APP.get("/tarefas")
async def listar_tarefas():
    lista_somente_id_titulo = []

    for tarefa in TAREFAS:
        id_tarefa = tarefa['id']
        titulo_tarefa = tarefa['titulo']

        lista_somente_id_titulo.append({id_tarefa: titulo_tarefa})

    return lista_somente_id_titulo

@APP.post("/tarefas")
async def post_tarefa(titulo: str, descricao: str):
    global TAREFAS

    tarefa_nova = criar_tarefa(titulo, descricao)
    TAREFAS.append(tarefa_nova)

    return {
        "mensagem": "Tarefa criada com sucesso",
        "tarefa": tarefa_nova
    }


# GET /tarefas/{id}: Visualizar tarefa específica
@APP.get("/tarefas/{id}")
async def tarefa_especifica(id: int):
    for tarefa in TAREFAS:
        if tarefa['id'] == id:
            return tarefa
        
    return {"mensagem": "Tarefa nao existe"}

# PUT /tarefas/{id}: Atualiza tarefa específica
@APP.put("/tarefas/{id}")
async def concluir_tarefa(id: int):
    for tarefa in TAREFAS:
        if tarefa['id'] == id and tarefa['concluida'] == False:
            tarefa['concluida'] = True
            tarefa['concluida_em'] = datetime.now()
            titulo = tarefa['titulo']

            resp = requests.post(f"http://localhost:8000/notificar?id={id}&titulo={titulo}")

            print(resp)

            return {"mensagem": "Tarefa atualizada"}
        
    return {"mensagem": "Tarefa nao existe"}

# DELETE /tarefas/{id}: Exclui tarefa
@APP.delete("/tarefas/{id}")
async def apagar_tarefa(id: int):
    global TAREFAS

    index = 0
    for tarefa in TAREFAS:
        if tarefa['id'] == id:
            TAREFAS.pop(indice)
            return {"mensagem": "Tarefa Removida"}
        indice += 1

    return {"mensagem": "Tarefa nao existe"}

@APP.get("/")
async def index():
    return {"mensagem": "Ola Mundo"}