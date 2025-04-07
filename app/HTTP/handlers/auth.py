from fastapi.routing import APIRouter
from fastapi import HTTPException

from app.container import container
from app.DTOs.token import TokenDTO, TokenResponseDTO

from domain.exceptions import NotFoundException, WrongPasswordException

auth_router = APIRouter()


@auth_router.post("/get_token/", response_model=TokenResponseDTO)
async def get_token(request: TokenDTO):
    try:
        token = await container.auth_service.verify_agencia_password(
            request.agencia, request.senha
        )
        return TokenResponseDTO(token=token)
    except (NotFoundException, WrongPasswordException) as e:
        raise HTTPException(401, str(e))
    except Exception as e:
        raise HTTPException(
            500, "Erro interno, se persistir entre em contato com nosso suporte"
        )
