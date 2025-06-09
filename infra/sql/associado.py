from psycopg_pool import AsyncConnectionPool

from domain.exceptions import NotFoundException
from domain.models.associado import Associado

from datetime import datetime


class AssociadoDb:
    pool: AsyncConnectionPool

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self.pool = pool

    async def get_associado_by_cpf(self, cpf: str) -> Associado:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                sql = """
                            SELECT
                                id, nome, cpf, nascimento, renda, cadastro
                            FROM associado
                            WHERE cpf = %s
                            """
                result = await cur.execute(sql, (cpf,))
                if result.rowcount == 0:
                    raise NotFoundException("CPF do associado")
                associado = await result.fetchone()
                if associado is None:
                    raise NotFoundException("CPF do associado")

                nascimento = datetime.combine(associado[3], datetime.min.time())
                cadastro = datetime.combine(associado[5], datetime.min.time())

                return Associado(
                    associado[0],
                    associado[1],
                    associado[2],
                    nascimento,
                    associado[4],
                    cadastro,
                )
