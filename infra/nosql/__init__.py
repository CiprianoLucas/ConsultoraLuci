from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi


class MongoConnection:
    def __init__(
        self,
        user: str,
        password: str,
        cluster: str,
        db_name: str,
        app_name: str = "DefaultApp",
    ):
        self.user = user
        self.password = password
        self.cluster = cluster
        self.db_name = db_name
        self.app_name = app_name
        self.client = None

    async def create_client(self) -> "MongoConnection":
        uri = (
            f"mongodb+srv://{self.user}:{self.password}@{self.cluster}/"
            f"?retryWrites=true&w=majority&appName={self.app_name}&tls=true"
        )

        self.client = AsyncIOMotorClient(
            uri,
            server_api=ServerApi("1"),
            serverSelectionTimeoutMS=10000,
            socketTimeoutMS=30000,
            connectTimeoutMS=10000,
        )
        return self

    def get_db(self):
        if not self.client:
            raise RuntimeError(
                "Mongo client has not been initialized. Call create_client() first."
            )
        return self.client[self.db_name]

    async def close_client(self):
        if self.client:
            self.client.close()
