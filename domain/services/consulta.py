from datetime import datetime, timedelta, timezone

import pandas as pd

from domain.models.associado import Associado
from infra.ia import IaRepository
from infra.nosql.consultas import ConsultaNoSql
from infra.nosql.score import ScoreNoSql
from infra.redis import CacheConnection
from infra.sql.associado import AssociadoDb
from infra.sql.colaborador import ColaboradorDb
from infra.sql.consultas import ConsultasDb


class ConsultaService:
    associado_db: AssociadoDb
    colaborador_db: ColaboradorDb
    consulta_db: ConsultasDb
    consulta_nosql: ConsultaNoSql
    score_nosql: ScoreNoSql
    fila: CacheConnection
    rota: str
    ia: IaRepository

    def __init__(
        self,
        associado_db: AssociadoDb,
        colaborador_db: ColaboradorDb,
        consulta_db: ConsultasDb,
        consulta_nosql: ConsultaNoSql,
        score_nosql: ScoreNoSql,
        fila: CacheConnection,
        rota: str,
        ia: IaRepository,
    ):
        self.associado_db = associado_db
        self.colaborador_db = colaborador_db
        self.consulta_db = consulta_db
        self.consulta_nosql = consulta_nosql
        self.score_nosql = score_nosql
        self.fila = fila
        self.rota = rota
        self.ia = ia

    async def list_consultas_agencia(self, agencia: int):
        result = await self.consulta_nosql.list_consultas_agencia(agencia)
        return result

    async def push_in_line(self, associado: str, agencia: int):
        await self.associado_db.get_associado_by_cpf(associado)
        await self.fila.push_para_fila(self.rota, f"{associado}_{agencia}")

    async def start_consulta(self, associado_cpf: str, agencia: int):
        hoje = datetime.now(timezone.utc)
        print(f"Agência {agencia} consultando cpf {associado_cpf} às {hoje}")
        consulta_recente = await self.consulta_nosql.ultima_consulta(
            associado_cpf, agencia
        )

        await self.consulta_nosql.delete(agencia, associado_cpf)

        if consulta_recente:
            data_consulta = consulta_recente["date_result"]

            if isinstance(data_consulta, str):
                data_consulta = datetime.fromisoformat(data_consulta)

            if data_consulta.tzinfo is None:
                data_consulta = data_consulta.replace(tzinfo=timezone.utc)

            hoje = datetime.now(timezone.utc)

            if hoje - data_consulta < timedelta(days=30):
                await self.consulta_nosql.insert(
                    agencia, associado_cpf, consulta_recente["result"], data_consulta
                )
                return

        associado = await self.associado_db.get_associado_by_cpf(associado_cpf)
        colaboradores = await self.colaborador_db.list_colaboradores_by_agencia_id(
            agencia
        )

        dados_associado = await self.get_dados_associado(associado.id)
        dados_colaborador = await self.get_dados_colaborador(colaboradores)

        dados_associado["nascimento"] = str(associado.nascimento)

        payload = {"associado": dados_associado, "colaboradores": dados_colaborador}

        response = self.ia.consultar_associado(payload)

        response["limite_credito"] = await self.verificar_limite_credito(associado)

        response["nome"] = associado.nome

        await self.consulta_nosql.insert(agencia, associado_cpf, response)

    async def verificar_limite_credito(self, associado: Associado) -> float:
        scores = await self.score_nosql.consultar_score(associado.cpf)

        fator = 0.4 if scores else 0.1

        meses_cadastro = self.meses_desde_cadastro(associado.cadastro)
        parcelas = min(meses_cadastro, 60)

        for score in scores:
            match score["company"]:
                case "SERASA":
                    score_val = score["result"].get("score")
                    if isinstance(score_val, (int, float)) or (
                        isinstance(score_val, str)
                        and score_val.replace(".", "", 1).isdigit()
                    ):
                        fator = fator * (float(score_val) / 1000)
                    else:
                        fator = fator * 0.5
                case "SPC":
                    nivel = score["result"].get("nivel")
                    if nivel == "alto":
                        fator = fator * 1
                    elif nivel == "medio":
                        fator = fator * 0.5
                    elif nivel == "baixo":
                        fator = fator * 0.3
                    else:
                        fator = fator * 0.5

                case _:
                    pass

        limite = fator * associado.renda * parcelas

        if limite < 500:
            limite = 500

        return limite
    
    def meses_desde_cadastro(self, cadastro: datetime) -> int:
        hoje = datetime.today()

        anos = hoje.year - cadastro.year
        meses = hoje.month - cadastro.month
        total_meses = anos * 12 + meses

        if hoje.day < cadastro.day:
            total_meses -= 1

        return total_meses

    async def get_dados_colaborador(self, colaboradores: list):

        result = []
        for colaborador in colaboradores:
            personalidades_colaborador = list(
                await self.consulta_db.list_personalidade_by_colaborador(colaborador[0])
            )
            creditos = pd.DataFrame(
                await self.consulta_db.list_creditos_by_colaborador(colaborador[0]),
                columns=["associado", "valor", "motivo", "personalide associado"],
            )
            result.append(
                {
                    "nome": colaborador[1],
                    "personalidades": personalidades_colaborador,
                    "creditos": creditos.to_dict(orient="records"),
                }
            )

        return result

    async def get_dados_associado(self, associado_id):
        personalidade = list(
            await self.consulta_db.list_personalidade_by_associado(associado_id)
        )
        creditos = pd.DataFrame(
            await self.consulta_db.list_creditos_by_associado(associado_id),
            columns=["motivo", "valor"],
        )
        compras = pd.DataFrame(
            await self.consulta_db.list_compras_by_associado(associado_id),
            columns=["segmento", "valor"],
        )
        feedbacks = list(
            await self.consulta_db.list_feedback_by_associado(associado_id)
        )

        result = {
            "personalidade": personalidade,
            "creditos": creditos.to_dict(orient="records"),
            "compras": compras.to_dict(orient="records"),
            "feedbacks": feedbacks,
        }

        return result
