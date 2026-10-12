from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def criar_hash_senha(senha: str) -> str:
    return password_hash.hash(senha)


def verificar_senha(
    senha: str,
    senha_hash: str
) -> bool:
    return password_hash.verify(senha, senha_hash)