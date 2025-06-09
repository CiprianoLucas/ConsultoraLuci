from functools import wraps

from psycopg import conninfo
from psycopg_pool import AsyncConnectionPool


class BaseDb:
    pool: AsyncConnectionPool = None

    def __init__(
        self,
        user=None,
        password=None,
        host=None,
        port=None,
        db_name=None,
        pool: AsyncConnectionPool = None,
    ):
        self.pool = pool
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name

    def _get_conninfo(self):
        return conninfo.make_conninfo(
            user=self.user,
            password=self.password,
            dbname=self.db_name,
            host=self.host,
            port=self.port,
            connect_timeout=10,
        )

    async def ensure_pool_open(self):
        if self.pool is None or self.pool.closed:
            self.pool = AsyncConnectionPool(conninfo=self._get_conninfo(), open=False)
            await self.pool.open()

    async def recreate_pool(self):
        if self.pool and not self.pool.closed:
            await self.pool.close()
        self.pool = AsyncConnectionPool(conninfo=self._get_conninfo(), open=False)
        await self.pool.open()

    def reconnect_on_failure(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                await self.ensure_pool_open()
                return await func(self, *args, **kwargs)
            except Exception as e:
                print(f"[WARN] Erro na primeira tentativa: {e}")
                print("[INFO] Recriando pool e tentando novamente...")
                await self.recreate_pool()
                return await func(self, *args, **kwargs)

        return wrapper
