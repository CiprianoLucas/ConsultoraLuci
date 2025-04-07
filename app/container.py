import boto3
from httpx import AsyncClient
from psycopg_pool import AsyncConnectionPool
from pydantic_settings import BaseSettings, SettingsConfigDict

from domain.services.auth import AuthService
from domain.services.consulta import ConsultaService
from infra.auth import AuthRepository
from infra.database import ConnectionPool
from infra.database.agencia import AgenciaDb
from infra.database.colaborador import ColaboradorDb
from infra.database.consultas import ConsultasDb
from infra.database.cooperado import CooperadoDb
from infra.ia import IaRepository
from infra.redis import CacheConnection


class Settings(BaseSettings):
    db_user: str
    db_host: str
    db_port: int = 5432
    db_name: str
    db_password: str
    redis_host: str
    redis_port: str
    redis_fila: str
    secret_key: str
    expiration: int
    iam_aws_key: str
    iam_aws_pass: str
    ia_id: str
    ia_alias: str

    model_config = SettingsConfigDict(env_file=".env")


class Container:
    auth_service: AuthService
    consulta_service: ConsultaService
    db_pool: AsyncConnectionPool
    settings: Settings = Settings()
    redis_connection: CacheConnection
    http_client: AsyncClient
    aws_client: boto3.Session

    async def load_dependencies(self):

        self.db_pool = await self.connect_to_database()
        self.redis_connection = self.connect_to_redis()
        self.http_client = AsyncClient()
        self.aws_client = boto3.Session(
            region_name="us-east-1",
            aws_access_key_id=self.settings.iam_aws_key,
            aws_secret_access_key=self.settings.iam_aws_pass,
        )

        auth_repository = AuthRepository(
            self.settings.secret_key, self.settings.expiration
        )

        ia_repository = IaRepository(
            self.aws_client, self.settings.ia_id, self.settings.ia_alias
        )

        agencia_db = AgenciaDb(self.db_pool)
        cooperado_db = CooperadoDb(self.db_pool)
        colaborador_db = ColaboradorDb(self.db_pool)
        consulta_db = ConsultasDb(self.db_pool)

        self.auth_service = AuthService(agencia_db, auth_repository)
        self.consulta_service = ConsultaService(
            cooperado_db,
            colaborador_db,
            consulta_db,
            self.redis_connection,
            self.settings.redis_fila,
            ia_repository,
        )

    async def connect_to_database(self) -> AsyncConnectionPool:
        pool = ConnectionPool(
            self.settings.db_user,
            self.settings.db_password,
            self.settings.db_host,
            self.settings.db_port,
            self.settings.db_name,
        )
        return await pool.create_pool()

    def connect_to_redis(self) -> CacheConnection:
        connection = CacheConnection(self.settings.redis_host, self.settings.redis_port)
        connection.create_connection()
        return connection

    async def close_container(self) -> None:
        await self.db_pool.close()
        await self.redis_connection.close()
        await self.http_client.aclose()


container: Container = Container()
