from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.di.container import get_container, init_logger
from presentation.routers import model_router, subscription_router, user_router


def init_routers(app: FastAPI):
    app.include_router(user_router)
    app.include_router(subscription_router)
    app.include_router(model_router)


def create_app() -> FastAPI:
    app = FastAPI(
        title="NeuroMesh",
        docs_url="/api/docs",
        description="NeuroMesh REST API",
        debug=True,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "HEAD", "OPTIONS", "DELETE"],
        allow_headers=[
            "Access-Control-Allow-Headers",
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Origin",
        ],
    )
    container = get_container()
    init_routers(app)
    init_logger()

    return app
