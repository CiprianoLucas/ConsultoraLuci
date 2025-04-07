import pandas as pd

from infra.database.colaborador import ColaboradorDb
from infra.database.consultas import ConsultasDb
from infra.database.cooperado import CooperadoDb
from infra.ia import IaRepository
from infra.redis import CacheConnection


class ConsultaService:
    cooperado_db: CooperadoDb
    colaborador_db: ColaboradorDb
    consulta_db: ConsultasDb
    fila: CacheConnection
    rota: str
    ia: IaRepository

    def __init__(
        self,
        cooperado_db: CooperadoDb,
        colaborador_db: ColaboradorDb,
        consulta_db: ConsultasDb,
        fila: CacheConnection,
        rota: str,
        ia: IaRepository,
    ):
        self.cooperado_db = cooperado_db
        self.colaborador_db = colaborador_db
        self.consulta_db = consulta_db
        self.fila = fila
        self.rota = rota
        self.ia = ia

    async def list_consultas_agencia(self, agencia: int):
        result = await self.consulta_db.list_consultas_agencia(agencia)
        return result

    async def push_in_line(self, cooperado: str, agencia: int):
        await self.cooperado_db.get_cooperado_by_cpf(cooperado)
        await self.fila.push_para_fila(self.rota, f"{cooperado}_{agencia}")

    async def start_consulta(self, cooperado: str, agencia: int):
        cooperado = await self.cooperado_db.get_cooperado_by_cpf(cooperado)
        colaboradores = await self.colaborador_db.list_colaboradores_by_agencia_id(
            agencia
        )

        dados_cooperado = await self.get_dados_cooperado(cooperado[0])
        dados_colaborador = await self.get_dados_colaborador(colaboradores)

        dados_cooperado["nascimento"] = str(cooperado[2])

        payload = {"cooperado": dados_cooperado, "colaboradores": dados_colaborador}

        response = self.ia.consultar_cooperado(payload)

        response["nome"] = cooperado[1]

        await self.consulta_db.insert(agencia, response)

        return

    async def get_dados_colaborador(self, colaboradores: list):

        result = []
        for colaborador in colaboradores:
            personalidades_colaborador = list(
                await self.consulta_db.list_personalidade_by_colaborador(colaborador[0])
            )
            creditos = pd.DataFrame(
                await self.consulta_db.list_creditos_by_colaborador(colaborador[0]),
                columns=["cooperado", "valor", "motivo", "personalide cooperado"],
            )
            result.append(
                {
                    "nome": colaborador[1],
                    "personalidades": personalidades_colaborador,
                    "creditos": creditos.to_dict(orient="records"),
                }
            )

        return result

    async def get_dados_cooperado(self, cooperado):
        personalidade = list(
            await self.consulta_db.list_personalidade_by_cooperado(cooperado)
        )
        creditos = pd.DataFrame(
            await self.consulta_db.list_creditos_by_cooperado(cooperado),
            columns=["motivo", "valor"],
        )
        compras = pd.DataFrame(
            await self.consulta_db.list_compras_by_cooperado(cooperado),
            columns=["segmento", "valor"],
        )
        feedbacks = list(await self.consulta_db.list_feedback_by_cooperado(cooperado))

        result = {
            "personalidade": personalidade,
            "creditos": creditos.to_dict(orient="records"),
            "compras": compras.to_dict(orient="records"),
            "feedbacks": feedbacks,
        }

        return result
