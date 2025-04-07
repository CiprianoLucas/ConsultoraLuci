import json
from typing import Any, Optional

from redis.asyncio import Redis


class CacheConnection:
    host: str
    port: int
    client: Redis

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def create_connection(self) -> None:
        self.client = Redis(host=self.host, port=self.port)

    async def push_para_fila(self, fila: str, valor: Any):
        try:
            serialized = json.dumps(valor)
            await self.client.rpush(fila, serialized)
        except Exception as e:
            raise Exception(f"Erro ao enviar para a fila: {str(e)}")

    async def consumir_da_fila(self, fila: str, timeout: int = 0) -> Optional[Any]:
        try:
            resultado = await self.client.blpop(fila, timeout=timeout)
            if resultado:
                _, value = resultado
                return json.loads(value)
            return None
        except Exception as e:
            raise Exception(f"Erro ao consumir da fila: {str(e)}")

    async def close(self) -> None:
        async with self.client as client:
            await client.close()
