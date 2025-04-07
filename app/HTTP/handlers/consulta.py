from fastapi import Depends, Response, status
from fastapi.routing import APIRouter

from app.container import container
from app.DTOs.consulta import ConsultarDTO
from app.HTTP.middlewares.auth import get_agencia_from_token

consulta_router = APIRouter()


@consulta_router.post("/consulta/", status_code=status.HTTP_204_NO_CONTENT)
async def consultar(
    request: ConsultarDTO,
    agencia: int = Depends(get_agencia_from_token),
):
    await container.consulta_service.push_in_line(request.cooperado, agencia)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@consulta_router.get("/consulta/", status_code=status.HTTP_200_OK)
async def consultas(agencia: int = Depends(get_agencia_from_token)):
    result = await container.consulta_service.list_consultas_agencia(agencia)
    return result or []
