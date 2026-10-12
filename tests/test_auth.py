
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.connection import Base
from app.database.models import User
from app.routers.auth import get_db
from app.security.password import criar_hash_senha
from app.routers.users import get_db as get_db_usuarios


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

Base.metadata.create_all(bind=engine_teste)


def get_db_teste():
    db = SessionTeste()
    try:
        yield db
    finally:
        db.close()



def test_login_com_sucesso():
    Base.metadata.drop_all(bind=engine_teste)
    Base.metadata.create_all(bind=engine_teste)

    db = SessionTeste()

    usuario = User(
        name="Usuario de Teste",
        email="teste@example.com",
        password_hash=criar_hash_senha("SenhaTeste123!"),
    )

    db.add(usuario)
    db.commit()
    db.close()

    app.dependency_overrides[get_db] = get_db_teste
    app.dependency_overrides[get_db_usuarios] = get_db_teste

    try:
        with TestClient(app) as cliente:
            resposta = cliente.post(
                "/auth/login",
                params={
                    "email": "teste@example.com",
                    "password": "SenhaTeste123!",
                },
            )

            assert resposta.status_code == 200
            assert "access_token" in resposta.json()
            assert resposta.json()["token_type"] == "bearer"

            token = resposta.json()["access_token"]

            resposta_usuario = cliente.get(
                "/users/me",
                headers={
                    "Authorization": f"Bearer {token}"
                },
            )

            assert resposta_usuario.status_code == 200
            assert resposta_usuario.json()["email"] == "teste@example.com"

    finally:
        app.dependency_overrides.pop(get_db, None)
        app.dependency_overrides.pop(get_db_usuarios, None)

