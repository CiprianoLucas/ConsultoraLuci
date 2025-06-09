from typing import Optional

from fastapi import Header, HTTPException

from app.container import container
from domain.exceptions import InvalidTokenException


def get_agencia_from_token(authorization: Optional[str] = Header(None)) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente ou malformado")
    token = authorization.split(" ")[1]
    try:
        return container.auth_service.get_agencia_from_token(token)
    except InvalidTokenException as e:
        raise HTTPException(401, str(e))
    except Exception:
        raise HTTPException(
            500, "Erro interno, se persistir entre em contato com nosso suporte"
        )
