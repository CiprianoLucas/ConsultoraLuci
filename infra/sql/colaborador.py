from psycopg_pool import AsyncConnectionPool


class ColaboradorDb:
    pool: AsyncConnectionPool

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self.pool = pool

    async def list_colaboradores_by_agencia_id(self, id: int) -> list:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                sql = """
                            SELECT
                                c.id, c.nome
                            FROM colaborador c
                            LEFT JOIN agencia_colaborador a
                                ON c.id = a.colaborador
                            WHERE a.agencia = %s
                            """
                result = await cur.execute(sql, (id,))
                if result.rowcount == 0:
                    raise Exception("colaboradores não enxontrada")
                colaboradores = await result.fetchall()
                if colaboradores is None:
                    raise Exception("colaboradores não enxontrada")
                return colaboradores
