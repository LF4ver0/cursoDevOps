from datetime import datetime, timezone
from app.modelo import Tarefa


def criar_tarefa_mock():
    return Tarefa(
        titulo="Tarefa teste",
        data_criacao=datetime.now().replace(microsecond=0),
    )


def test_nova_tarefa():
    t = criar_tarefa_mock()

    assert t.get_id() == None
    assert t.titulo == "Tarefa teste"
    assert t.descricao == None
    assert t.data_criacao == datetime.now().replace(microsecond=0)
    assert t.data_conclusao == None
    assert t.concluida == False


# Implementar teste unitário para verificar se a tarefa foi concluida


def test_tarefa_concluida():
    t = criar_tarefa_mock()

    t.finalizar()
    assert t.concluida == True
    assert t.data_conclusao == datetime.now().astimezone(timezone.utc).replace(microsecond=0)