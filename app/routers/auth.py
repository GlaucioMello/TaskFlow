from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import User
from app.security.password import verificar_senha
from app.auth.jwt import criar_token_acesso


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    usuario = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    if not verificar_senha(password, usuario.password_hash):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    token = criar_token_acesso(usuario.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }