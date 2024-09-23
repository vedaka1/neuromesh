import logging.handlers
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.di.container import get_container, init_logger, init_loki_logger
from infrastructure.tasks.main import broker
from presentation.exc_handlers import init_exc_handlers
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
    get_container()
    await broker.startup()
    yield
    await broker.shutdown()


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
    init_exc_handlers(app)
    init_logger()
    #handler = init_loki_logger(app_name="api")
    #logging.getLogger().addHandler(handler)
    #logging.getLogger("uvicorn.access").addHandler(handler)
    return app
