from fastapi.routing import APIRouter

from app.container import container
from app.DTOs.token import TokenDTO, TokenResponseDTO

auth_router = APIRouter()


@auth_router.post("/get_token/", response_model=TokenResponseDTO)
async def get_token(request: TokenDTO):
    token = await container.auth_service.verify_agencia_password(
        request.agencia, request.senha
    )
    return TokenResponseDTO(token=token)
