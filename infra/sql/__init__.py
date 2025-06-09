from psycopg import conninfo
from psycopg_pool import AsyncConnectionPool


class ConnectionPool:
    def __init__(self, user: str, password: str, host: str, port: int, db_name: str):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name

    async def create_pool(self) -> AsyncConnectionPool:
        pool = AsyncConnectionPool(
            conninfo=conninfo.make_conninfo(
                user=self.user,
                password=self.password,
                dbname=self.db_name,
                host=self.host,
                port=self.port,
            ),
            open=False,
        )
        await pool.open()
        return pool

    async def close_pool(self, pool: AsyncConnectionPool):
        await pool.close()
