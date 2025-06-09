import boto3
from httpx import AsyncClient
from psycopg_pool import AsyncConnectionPool
from pydantic_settings import BaseSettings, SettingsConfigDict

from domain.services.auth import AuthService
from domain.services.consulta import ConsultaService
from infra.auth import AuthRepository
from infra.ia import IaRepository
from infra.nosql import MongoConnection
from infra.nosql.consultas import ConsultaNoSql
from infra.nosql.score import ScoreNoSql
from infra.redis import CacheConnection
from infra.sql import BaseDb
from infra.sql.agencia import AgenciaDb
from infra.sql.associado import AssociadoDb
from infra.sql.colaborador import ColaboradorDb
from infra.sql.consultas import ConsultasDb


class Settings(BaseSettings):
    db_user: str
    db_host: str
    db_port: int = 5432
    db_name: str
    db_password: str
    redis_host: str
    redis_port: str
    redis_password: str = "default"
    redis_username: str = "default"
    redis_decode: bool = True
    redis_fila: str
    secret_key: str
    expiration: int
    iam_aws_key: str
    iam_aws_pass: str
    ia_id: str
    ia_alias: str
    nosql_user: str
    nosql_password: str
    nosql_cluster: str
    nosql_db_name: str
    nosql_app_name: str = "default"

    model_config = SettingsConfigDict(env_file=".env")


class Container:
    auth_service: AuthService
    consulta_service: ConsultaService
    db_pool: AsyncConnectionPool
    mongo_connection: MongoConnection
    settings: Settings = Settings()
    redis_connection: CacheConnection
    http_client: AsyncClient
    aws_client: boto3.Session

    async def load_dependencies(self):

        self.db_pool = await self.connect_to_sql_database()
        self.mongo_connection = await self.connect_to_nosql_database()
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

        db_parameters = {
            "pool": self.db_pool,
            "user": self.settings.db_user,
            "password": self.settings.db_password,
            "host": self.settings.db_host,
            "port": self.settings.db_port,
            "db_name": self.settings.db_name,
        }

        agencia_db = AgenciaDb(**db_parameters)
        associado_db = AssociadoDb(**db_parameters)
        colaborador_db = ColaboradorDb(**db_parameters)
        consulta_db = ConsultasDb(**db_parameters)

        nosql_db = self.mongo_connection.get_db()

        consulta_nosql = ConsultaNoSql(nosql_db)
        score_nosql = ScoreNoSql(nosql_db)

        self.auth_service = AuthService(agencia_db, auth_repository)
        self.consulta_service = ConsultaService(
            associado_db,
            colaborador_db,
            consulta_db,
            consulta_nosql,
            score_nosql,
            self.redis_connection,
            self.settings.redis_fila,
            ia_repository,
        )

    async def connect_to_sql_database(self) -> AsyncConnectionPool:
        base_db = BaseDb(
            self.settings.db_user,
            self.settings.db_password,
            self.settings.db_host,
            self.settings.db_port,
            self.settings.db_name,
        )
        await base_db.recreate_pool()
        return base_db.pool

    async def connect_to_nosql_database(self) -> MongoConnection:
        pool = MongoConnection(
            self.settings.nosql_user,
            self.settings.nosql_password,
            self.settings.nosql_cluster,
            self.settings.nosql_db_name,
            self.settings.nosql_app_name,
        )
        return await pool.create_client()

    def connect_to_redis(self) -> CacheConnection:
        connection = CacheConnection(
            self.settings.redis_host,
            self.settings.redis_port,
            self.settings.redis_password,
            self.settings.redis_username,
            self.settings.redis_decode,
        )
        connection.create_connection()
        return connection

    async def close_container(self) -> None:
        await self.db_pool.close()
        await self.mongo_connection.close_client()
        await self.redis_connection.close()
        await self.http_client.aclose()


container: Container = Container()
