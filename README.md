# Curso DevOps - Gerenciador de Tarefas (API REST)

API REST desenvolvida em Python para gerenciamento de tarefas (*To-Do List*), desenvolvida como projeto prático do curso/módulo de extensão em DevOps. O projeto conta com pipelines de CI/CD automatizados, integração com banco de dados relacional e suporte a containerização.

---

## 1. Descrição da Aplicação

A aplicação consiste em uma API de gerenciamento de tarefas com operações de CRUD e persistência de dados.

### Principais Funcionalidades:
- **`GET /`**: Rota raiz de boas-vindas (*health check* simples).
- **`GET /autor`**: Informa o autor responsável pela aplicação.
- **`GET /tarefas`**: Lista todas as tarefas cadastradas no banco de dados.
- **`POST /tarefas`**: Cria uma nova tarefa com título, descrição e data de criação.
- **`GET /tarefas/{id_tarefa}`**: Consulta os detalhes de uma tarefa específica por ID.
- **`PUT /tarefas/{id_tarefa}`**: Marca uma tarefa como finalizada/concluída, registrando a data de conclusão.
- **`DELETE /tarefas/{id_tarefa}`**: Remove uma tarefa do banco de dados.
- **Serviço de Notificações**: Módulo auxiliar (`app/notificacao.py`) com endpoint `/notificar` para envio de notificações de conclusão de tarefas.

---

## 2. Tecnologias Utilizadas

- **Linguagem:** [Python](https://www.python.org/) (versão 3.12+)
- **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/) (com suporte a ASGI e validação via Pydantic)
- **Persistência de Dados e ORM:**
  - [SQLModel](https://sqlmodel.tiangolo.com/) / [SQLAlchemy](https://www.sqlalchemy.org/)
  - [PostgreSQL](https://www.postgresql.org/) com driver [Psycopg 3](https://www.psycopg.org/)
- **Testes e Qualidade de Código:**
  - [Pytest](https://docs.pytest.org/) e `pytest-cov` (testes automatizados e cobertura)
  - [Pylint](https://pylint.pycqa.org/) e [Ruff](https://beta.ruff.rs/) (análise estática e linting)
  - [Bandit](https://bandit.readthedocs.io/) (análise de segurança de código)
- **Containerização e Infraestrutura:**
  - [Docker](https://www.docker.com/) (Dockerfile para empacotamento da aplicação)
  - [Kubernetes](https://kubernetes.io/) (manifesto `pod.yaml` para Pods e Services)
  - [Nginx](https://nginx.org/) (`default.conf` configurado como reverse proxy)
- **CI/CD:**
  - [GitHub Actions](https://github.com/features/actions) (integração contínua com lint/testes, entrega contínua com publicação no Docker Hub e deploy contínuo via hook no Render)

---

## 3. Instruções para Execução Local

### Pré-requisitos
- Python 3.12 ou superior instalado.
- PostgreSQL em execução (localmente ou via Docker).
- Git instalado.

---

### Passo 1: Clonar o Repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd cursoDevOps
```

---

### Passo 2: Criar e Ativar o Ambiente Virtual
- **No Linux/macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

- **No Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

---

### Passo 3: Instalar as Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Passo 4: Configurar as Variáveis de Ambiente
A aplicação exige a configuração das credenciais e endereço de conexão com o PostgreSQL:

- **No Linux/macOS:**
  ```bash
  export DATABASE_USERNAME="devops"
  export DATABASE_PASSWORD="password"
  export DATABASE_ADDRESS="localhost"
  export DATABASE="devops"
  ```

- **No Windows (PowerShell):**
  ```powershell
  $env:DATABASE_USERNAME="devops"
  $env:DATABASE_PASSWORD="password"
  $env:DATABASE_ADDRESS="localhost"
  $env:DATABASE="devops"
  ```

> **Dica:** Você pode iniciar uma instância do PostgreSQL rapidamente com Docker:
> ```bash
> docker run --name postgres-devops -e POSTGRES_USER=devops -e POSTGRES_PASSWORD=password -e POSTGRES_DB=devops -p 5432:5432 -d postgres
> ```

---

### Passo 5: Executar a Aplicação
Com o ambiente ativado e as variáveis configuradas, inicie o servidor:

```bash
fastapi dev app/api.py
```
*ou via Uvicorn:*
```bash
uvicorn app.api:APP --host 0.0.0.0 --port 8000 --reload
```

Acesse a documentação interativa da API no navegador:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Passo 6: Executar Testes e Lint
Para rodar a suíte de testes unitários:
```bash
pytest --rootdir app
```

Para rodar a verificação de lint com Pylint:
```bash
pylint app
```

---

### Execução via Docker (Opcional)
Se preferir executar o container da aplicação diretamente com Docker:

1. **Construir a imagem:**
   ```bash
   docker build -t tarefas:latest .
   ```

2. **Executar o container:**
   ```bash
   docker run -p 8000:8000 \
     -e DATABASE_USERNAME="devops" \
     -e DATABASE_PASSWORD="password" \
     -e DATABASE_ADDRESS="host.docker.internal" \
     -e DATABASE="devops" \
     tarefas:latest
   ```
