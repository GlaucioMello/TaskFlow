from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.connection import Base
from app.database.models import User
from app.routers.auth import get_db as get_db_auth
from app.routers.users import get_db as get_db_usuarios
from app.routers.tasks import get_db as get_db_tarefas
from app.security.password import criar_hash_senha
from app.auth.jwt import criar_token_acesso


engine_teste = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessionTeste = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_teste,
)


def get_db_teste():
    db = SessionTeste()
    try:
        yield db
    finally:
        db.close()


def test_criar_e_listar_tarefas():
    Base.metadata.drop_all(bind=engine_teste)
    Base.metadata.create_all(bind=engine_teste)

    db = SessionTeste()

    usuario = User(
        name="Usuario de Teste",
        email="tarefas@example.com",
        password_hash=criar_hash_senha("SenhaTeste123!"),
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    usuario_id = usuario.id
    db.close()

    app.dependency_overrides[get_db_auth] = get_db_teste
    app.dependency_overrides[get_db_usuarios] = get_db_teste
    app.dependency_overrides[get_db_tarefas] = get_db_teste

    try:
        with TestClient(app) as cliente:
            token = criar_token_acesso(usuario_id)

            headers = {
                "Authorization": f"Bearer {token}"
            }

            resposta_criar = cliente.post(
                "/tasks/",
                headers=headers,
                json={
                    "title": "Estudar testes automatizados",
                    "description": "Testar a criação de tarefas",
                },
            )

            assert resposta_criar.status_code == 201, resposta_criar.text

            tarefa = resposta_criar.json()

            assert tarefa["title"] == "Estudar testes automatizados"
            assert tarefa["description"] == "Testar a criação de tarefas"
            assert tarefa["completed"] is False
            assert tarefa["user_id"] == usuario_id

            resposta_listar = cliente.get(
                "/tasks/",
                headers=headers,
            )

            assert resposta_listar.status_code == 200, resposta_listar.text

            tarefas = resposta_listar.json()

            assert len(tarefas) == 1
            assert tarefas[0]["id"] == tarefa["id"]
            resposta_atualizar = cliente.put(
                f"/tasks/{tarefa['id']}",
                headers=headers,
                json={
                    "title": "Estudar testes automatizados - atualizado",
                    "description": "Testar atualização de tarefas",
                    "completed": True,
                },
            )

            assert resposta_atualizar.status_code == 200, resposta_atualizar.text
            assert resposta_atualizar.json()["title"] == (
                "Estudar testes automatizados - atualizado"
            )
            assert resposta_atualizar.json()["completed"] is True

            resposta_excluir = cliente.delete(
                f"/tasks/{tarefa['id']}",
                headers=headers,
            )

            assert resposta_excluir.status_code in (200, 204), resposta_excluir.text

            resposta_buscar = cliente.get(
                f"/tasks/{tarefa['id']}",
                headers=headers,
            )

            assert resposta_buscar.status_code == 404

    finally:
        app.dependency_overrides.pop(get_db_auth, None)
        app.dependency_overrides.pop(get_db_usuarios, None)
        app.dependency_overrides.pop(get_db_tarefas, None)