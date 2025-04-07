from psycopg_pool import AsyncConnectionPool
from domain.exceptions import NotFoundException


class AgenciaDb:
    pool: AsyncConnectionPool

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self.pool = pool

    async def get_senha_by_agencia_id(self, id: int) -> str:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                sql = """
                            SELECT
                                senha
                            FROM agencia
                            WHERE id = %s
                            """
                result = await cur.execute(sql, (id,))
                if result.rowcount == 0:
                    raise NotFoundException("agência")
                agencia = await result.fetchone()
                if agencia is None:
                    raise NotFoundException("agência")
                return agencia[0]
