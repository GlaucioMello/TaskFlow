from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from app.auth.jwt import SECRET_KEY, ALGORITHM


security = HTTPBearer()


def obter_usuario_id(
    credenciais: HTTPAuthorizationCredentials = Depends(security)
):
    token = credenciais.credentials

    try:
        dados = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = dados.get("sub")

        if usuario_id is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido."
            )

        return int(usuario_id)

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado."
        )