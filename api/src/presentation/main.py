import asyncio
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine

from infrastructure.di.container import get_container, init_logger
from infrastructure.persistence.models import Base
from presentation.routers import model_router, subscription_router, user_router


def init_di(app: FastAPI) -> None:
    container = get_container()
    setup_dishka(container, app)


def init_routers(app: FastAPI):
    app.include_router(user_router)
    app.include_router(subscription_router)
    app.include_router(model_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = get_container()
    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


def create_app() -> FastAPI:

    app = FastAPI(
        title="NeuroMesh",
        docs_url="/api/docs",
        description="NeuroMesh REST API",
        debug=True,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "HEAD", "OPTIONS", "DELETE", "PUT", "PATCH"],
        allow_headers=[
            "Access-Control-Allow-Headers",
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Origin",
        ],
    )
    init_di(app)
    init_routers(app)
    init_logger()
    return app
