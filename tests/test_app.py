import pytest

from fastapi.testclient import TestClient
from app.api import APP, criar_sessao
from datetime import datetime
from sqlmodel import SQLModel, Session, create_engine

DATA = None
DATA_CONCLUSAO = None
BANCO = create_engine("sqlite:///banco.db", connect_args={"check_same_thread": False})

@pytest.fixture(name="sessao")
def fixture_sessao():
    SQLModel.metadata.create_all(BANCO)

    with Session(BANCO) as s:
        yield s

    SQLModel.metadata.drop_all(BANCO)

@pytest.fixture(name='cliente')
def fixture_cliente(sessao: Session):
    def get_sessao():
        return sessao

    APP.dependency_overrides[criar_sessao] = get_sessao

    cliente = TestClient(APP)
    yield cliente

    APP.dependency_overrides.clear()

def test_index(cliente: TestClient):
    resposta = cliente.get("/")
    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Olá, mundo!"}


# 1. Implementar um teste unitário para a rota /tarefas (GET)
def test_tarefas_get(cliente: TestClient):
    resposta = cliente.get("/tarefas")
    assert resposta.status_code == 200

    # Testando se a rota retorna uma lista vazia
    assert resposta.json() == []


# 2. Implementar um teste unitário para a rota /tarefas (POST)
def test_tarefas_post(cliente: TestClient):
    global DATA
    resposta = cliente.post("/tarefas?titulo=teste&descricao=teste")
    DATA = datetime.now().replace(microsecond=0).isoformat() + "Z"

    assert resposta.status_code == 201
    assert resposta.json() == {"mensagem": "OK"}

    resposta = cliente.get("/tarefas")
    assert resposta.json() == [
        {
            "_id": 1,
            "descricao": "teste",
            "data_criacao": DATA,
            "concluida": False,
            "titulo": "teste",
            "data_conclusao": None
        }
    ]

# 3. Implementar um teste unitário para a rota /tarefas/{id} (PUT)
def test_tarefas_put(cliente: TestClient):
    # Crio a tarefa
    resposta = cliente.post("/tarefas?titulo=teste&descricao=teste")

    # Finalizo a tarefa
    resposta = cliente.put("/tarefas/1")
    DATA_CONCLUSAO = datetime.now().replace(microsecond=0).isoformat() + "Z"
    assert resposta.json() == {"mensagem": "Tarefa atualizada"}

    resposta = cliente.put("/tarefas/0")
    assert resposta.json() == {"mensagem": "Tarefa não existe"}

    resposta = cliente.get("/tarefas/1")
    assert resposta.status_code == 200
    assert resposta.json() ==  {
        "_id": 1,
        "descricao": "teste",
        "data_criacao": DATA,
        "concluida": True,
        "titulo": "teste",
        "data_conclusao": str(DATA_CONCLUSAO)
    }


# 5. Implementar um teste unitário para a rota /tarefas/{id} (DELETE)
def test_tarefas_delete(cliente: TestClient):
    # Crio a tarefa
    resposta = cliente.post("/tarefas?titulo=teste&descricao=teste")

    resposta = cliente.delete("/tarefas/0")
    assert resposta.json() == {"mensagem": "Tarefa não existe"}

    resposta = cliente.delete("/tarefas/1")
    assert resposta.json() == {"mensagem": "Tarefa removida"}

    resposta = cliente.get("/tarefas")
    assert resposta.json() == []

# 2. Criar um teste unitário para verificar se a rota
# está produzindo o resultado esperado
def test_autor(cliente: TestClient):
    resposta = cliente.get("/autor")
    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Lucas Felipe"}
