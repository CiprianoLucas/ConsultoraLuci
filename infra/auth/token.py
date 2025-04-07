import json
from datetime import datetime, timedelta

import jwt


def create_token(subject: str | dict, secret_key: str, expitarion: int) -> str:
    expiration = datetime.utcnow() + timedelta(minutes=expitarion)
    payload = {"sub": json.dumps(subject), "exp": expiration}
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def verify_token(token: str, secret_key: str) -> int:
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return json.loads(payload.get("sub"))
    except jwt.ExpiredSignatureError:
        raise Exception(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise Exception(status_code=401, detail="Token inválido")
