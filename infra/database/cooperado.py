from psycopg_pool import AsyncConnectionPool
from domain.exceptions import NotFoundException


class CooperadoDb:
    pool: AsyncConnectionPool

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self.pool = pool

    async def get_cooperado_by_cpf(self, cpf: str) -> object:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                sql = """
                            SELECT
                                id, nome, nascimento
                            FROM cooperado
                            WHERE cpf = %s
                            """
                result = await cur.execute(sql, (cpf,))
                if result.rowcount == 0:
                    raise NotFoundException("CPF do cooperado")
                cooperado = await result.fetchone()
                if cooperado is None:
                    raise NotFoundException("CPF do cooperado")
                return cooperado
