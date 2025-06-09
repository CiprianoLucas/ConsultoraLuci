from datetime import datetime, timezone
from typing import List

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase


class ConsultaNoSql:
    db: AsyncIOMotorDatabase
    collection: AsyncIOMotorCollection

    def __init__(self, db):
        self.db = db
        self.collection = self.db["consulta"]

    async def insert(
        self,
        agencia: int,
        cpf: str,
        resultado: dict,
        last_consultation: datetime = None,
    ):
        now = datetime.now(timezone.utc)

        doc = {
            "agencia": agencia,
            "cpf": cpf,
            "result": resultado,
            "date_insert": now,
            "date_result": (last_consultation if last_consultation else now),
        }
        try:
            await self.collection.insert_one(doc)
        except Exception as e:
            raise Exception(str(e))

    async def delete(self, agencia: str, cpf: str):
        try:
            result = await self.collection.delete_many({"agencia": agencia, "cpf": cpf})
            return result.deleted_count
        except Exception as e:
            raise Exception(str(e))

    async def ultima_consulta(self, cpf: str, agencia: int):
        doc = await self.collection.find_one(
            {"cpf": cpf, "agencia": agencia}, sort=[("date_insert", -1)]
        )
        return doc

    async def list_consultas_agencia(self, id: str) -> List[dict]:
        cursor = self.collection.find({"agencia": id}, {"_id": 0, "result": 1}).sort(
            "_id", -1
        )

        resultados = []
        async for doc in cursor:
            resultados.append(doc["result"])
        return resultados
