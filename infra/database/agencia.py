from psycopg_pool import AsyncConnectionPool


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
                    raise Exception("agencia não enxontrada")
                agencia = await result.fetchone()
                if agencia is None:
                    raise Exception("agencia não enxontrada")
                return agencia[0]
