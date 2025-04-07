from .password import verify_password
from .token import create_token, verify_token


class AuthRepository:
    secret_key: str
    expiration: int

    def __init__(self, secret_key: str, expiration: int):
        self.secret_key = secret_key
        self.expiration = expiration

    def verify_password(self, senha: str, senha_hash: str) -> bool:
        return verify_password(senha, senha_hash)

    def create_token(self, subject: str | dict) -> str:
        return create_token(subject, self.secret_key, self.expiration)

    def verify_token(self, token: str) -> dict:
        return verify_token(token, self.secret_key)
