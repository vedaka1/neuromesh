from fastapi import FastAPI

from infrastructure.di.container import get_container


def create_app() -> FastAPI:
    container = get_container()
    app = FastAPI(
        title="NeuroMesh",
        docs_url="/api/docs",
        description="NeuroMesh REST API",
        debug=True,
    )
    return app
