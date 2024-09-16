import logging
from functools import lru_cache
from multiprocessing import Queue

import logging_loki
from httpx import AsyncClient

users = {}


@lru_cache(1)
def init_logger() -> None:
    logging.basicConfig(
        # filename="log.log",
        level=logging.INFO,
        encoding="UTF-8",
        format="%(asctime)s %(levelname)s: %(message)s",
    )


@lru_cache(1)
def init_loki_logger(app_name: str = "app"):
    return logging_loki.LokiQueueHandler(
        Queue(-1),
        url="http://loki:3100/loki/api/v1/push",
        tags={"application": app_name},
        version="1",
    )


@lru_cache(1)
def init_client() -> AsyncClient:
    return AsyncClient(
        base_url="http://api:8000",
        timeout=25,
    )
