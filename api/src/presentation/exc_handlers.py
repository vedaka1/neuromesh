import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain.exceptions.base import ApplicationException

logger = logging.getLogger()


async def app_exc_handler(request: Request, exc: ApplicationException) -> JSONResponse:
    logger.error(msg="Handle error", exc_info=exc, extra={"error": exc})
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


async def unknown_exception_handler(request: Request, err: Exception) -> JSONResponse:
    logger.error(msg="Handle error", exc_info=err, extra={"error": err})
    return JSONResponse(status_code=500, content={"detail": "Unknown error occurred"})


def init_exc_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationException, app_exc_handler)
    app.add_exception_handler(Exception, unknown_exception_handler)
