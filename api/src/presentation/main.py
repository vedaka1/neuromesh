from fastapi import FastAPI

from infrastructure.di.container import get_container
from presentation.routers import user_router


def init_routers(app: FastAPI):
    app.include_router(user_router)


def create_app() -> FastAPI:
    app = FastAPI(
        title="NeuroMesh",
        docs_url="/api/docs",
        description="NeuroMesh REST API",
        debug=True,
    )

    container = get_container()
    init_routers(app)

    return app
