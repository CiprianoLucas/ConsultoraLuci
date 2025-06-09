import json

from psycopg_pool import AsyncConnectionPool


class ConsultasDb:
    pool: AsyncConnectionPool

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self.pool = pool

    async def insert(self, agencia: int, resultado: dict):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                sql = """
                    INSERT INTO consulta (
                        agencia,
                        resultado
                    ) VALUES (
                        %s, %s::jsonb
                    )
                """
                params = (agencia, json.dumps(resultado, ensure_ascii=False))

                try:
                    await cur.execute(sql, params)
                except Exception as e:
                    raise Exception(str(e))

    async def list_compras_by_associado(self, id: str) -> list:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                sql = """
                            SELECT
                                segmento, valor
                            FROM compras
                            WHERE associado = %s
                            """
                result = await cur.execute(sql, (id,))
                return await result.fetchall()

    async def list_creditos_by_associado(self, id: str) -> list:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                sql = """
                            SELECT
                                motivo, valor
                            FROM creditos
                            WHERE associado = %s
                            """
                result = await cur.execute(sql, (id,))
                return await result.fetchall()

    async def list_feedback_by_associado(self, id: str) -> list:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                sql = """
                            SELECT
                                descricao
                            FROM feedback
                            WHERE associado = %s
                            """
                result = await cur.execute(sql, (id,))
                rows = await result.fetchall()
                return [row[0] for row in rows]

    async def list_personalidade_by_associado(self, id: str) -> list:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                sql = """
                            SELECT
                                p.descricao
                            FROM personalidade p
                            LEFT JOIN personalidade_associado pc
                                ON p.id = pc.personalidade
                            WHERE pc.associado = %s
                            """
                result = await cur.execute(sql, (id,))
                rows = await result.fetchall()
                return [row[0] for row in rows]

    async def list_personalidade_by_colaborador(self, id: int) -> list:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                sql = """
                            SELECT
                                p.descricao
                            FROM personalidade p
                            LEFT JOIN personalidade_colaborador pc
                                ON p.id = pc.personalidade
                            WHERE pc.colaborador =(%s)
                            """
                result = await cur.execute(sql, (id,))
                rows = await result.fetchall()
                return [row[0] for row in rows]

    async def list_creditos_by_colaborador(self, id: int) -> list:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                sql = """
                    SELECT
                        c.associado,
                        c.valor,
                        c.motivo,
                        STRING_AGG(p.descricao, ', ') AS "personalidade associado"
                    FROM creditos c
                    LEFT JOIN personalidade_associado pc ON c.associado = pc.associado
                    LEFT JOIN personalidade p ON pc.personalidade = p.id
                    WHERE c.colaborador = %s
                    GROUP BY c.associado, c.valor, c.motivo;
                    """
                result = await cur.execute(sql, (id,))
                return await result.fetchall()

    async def list_consultas_agencia(self, id: int) -> list:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                sql = """
                    SELECT
                        resultado
                    FROM consulta
                    WHERE agencia = %s
                    ORDER BY id DESC
                    ;
                    """
                result = await cur.execute(sql, (id,))
                rows = await result.fetchall()
                return [row[0] for row in rows]
