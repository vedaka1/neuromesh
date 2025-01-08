import logging

from domain.exceptions.base import ApplicationException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


async def app_exc_handler(request: Request, exc: ApplicationException) -> JSONResponse:
    logging.error(msg='Handle error', exc_info=exc, extra={'error': exc})
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.message})


async def unknown_exception_handler(request: Request, err: Exception) -> JSONResponse:
    logging.error(msg='Handle error', exc_info=err, extra={'error': err})
    return JSONResponse(status_code=500, content={'detail': 'Unknown error occurred'})


def init_exc_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationException, app_exc_handler)  # type: ignore
    app.add_exception_handler(Exception, unknown_exception_handler)
