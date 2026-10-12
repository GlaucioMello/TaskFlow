from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def criar_token_acesso(user_id: int) -> str:
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados = {"sub": str(user_id), "exp": expiracao}
    token = jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)
    return token
