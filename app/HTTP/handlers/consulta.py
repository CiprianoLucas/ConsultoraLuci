from fastapi import Depends, HTTPException, Response, status
from fastapi.routing import APIRouter

from app.container import container
from app.DTOs.consulta import ConsultarDTO
from app.HTTP.middlewares.auth import get_agencia_from_token
from domain.exceptions import NotFoundException

consulta_router = APIRouter()


@consulta_router.post("/consulta/", status_code=status.HTTP_204_NO_CONTENT)
async def consultar(
    request: ConsultarDTO,
    agencia: int = Depends(get_agencia_from_token),
):
    try:
        await container.consulta_service.push_in_line(request.associado, agencia)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception:
        raise HTTPException(
            500, "Erro interno, se persistir entre em contato com nosso suporte"
        )


@consulta_router.get("/consulta/", status_code=status.HTTP_200_OK)
async def consultas(agencia: int = Depends(get_agencia_from_token)):
    try:
        result = await container.consulta_service.list_consultas_agencia(agencia)
        return result or []
    except NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception:
        raise HTTPException(
            500, "Erro interno, se persistir entre em contato com nosso suporte"
        )
