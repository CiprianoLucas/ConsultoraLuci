from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.container import container
from app.HTTP.handlers.auth import auth_router
from app.HTTP.handlers.consulta import consulta_router
from app.HTTP.middlewares.cors import add_cors_middleware

# from worker import start_worker_in_thread


@asynccontextmanager
async def lifespan(app: FastAPI):
    await container.load_dependencies()
    # start_worker_in_thread()
    # wait until shutdown
    yield
    # runs after shutdown
    await container.close_container()


app = FastAPI(lifespan=lifespan)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Minha API",
        version="1.0.0",
        description="API com autenticação",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(auth_router, tags=["auth"])
app.include_router(consulta_router, tags=["consulta"])

add_cors_middleware(app)
