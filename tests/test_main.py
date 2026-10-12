
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_rota_inicial():
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "TaskFlow API está funcionando!"
    assert resposta.json()["versao"] == "1.0.0"


def test_rota_health():
    resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "online"

def test_listar_tarefas_sem_token():
    resposta = client.get("/tasks/")

    assert resposta.status_code in (401, 403)


def test_login_com_credenciais_invalidas():
    resposta = client.post("/auth/login",
        params={"email": "naoexiste@example.com","password": "senha_incorreta_123"})

    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "E-mail ou senha inválidos."
