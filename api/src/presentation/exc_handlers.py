from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain.exceptions.base import ApplicationException


async def app_exc_handler(request: Request, exc: ApplicationException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


def init_exc_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationException, app_exc_handler)
