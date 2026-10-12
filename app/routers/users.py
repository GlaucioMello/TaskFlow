from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.security.password import criar_hash_senha
from app.database.connection import SessionLocal
from app.database.models import User
from app.schemas.user import UserCreate, UserResponse
from app.auth.dependencies import obter_usuario_id


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_existing = db.query(User).filter(User.email == user.email).first()
    if user_existing:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado.")

    password_hash = criar_hash_senha(user.password)

    new_user = User(name=user.name, email=user.email, password_hash=password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db),user_id: int = Depends(obter_usuario_id)):
    users = db.query(User).all()
    return users

@router.get("/me", response_model=UserResponse)
def my_user(user_id: int = Depends(obter_usuario_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, dados: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    user.name = dados.name
    user.email = dados.email
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    db.delete(user)
    db.commit()
    return {"detail": "Usuário excluído com sucesso."}
