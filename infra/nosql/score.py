from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase


class ScoreNoSql:
    db: AsyncIOMotorDatabase
    collection: AsyncIOMotorCollection

    def __init__(self, db):
        self.db = db
        self.collection = self.db["score"]

    async def consultar_score(self, cpf: str):

        cursor = self.collection.find({"cpf": cpf}, {"_id": 0, "result": 1, "company": 1})
        resultados = []
        async for doc in cursor:
            resultados.append(doc["result"])

        return resultados
