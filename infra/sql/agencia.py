from domain.exceptions import NotFoundException
from infra.sql import BaseDb


class AgenciaDb(BaseDb):
    @BaseDb.reconnect_on_failure
    async def get_senha_by_agencia_id(self, id: int) -> str:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                sql = """
                    SELECT senha FROM agencia WHERE id = %s
                """
                await cur.execute(sql, (id,))
                agencia = await cur.fetchone()
                if agencia is None:
                    raise NotFoundException("agência")
                return agencia[0]
