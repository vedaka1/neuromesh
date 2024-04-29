import logging
from functools import lru_cache

from httpx import AsyncClient

users = {}


@lru_cache(1)
def init_logger() -> logging.Logger:
    logging.basicConfig(
        # filename="log.log",
        level=logging.INFO,
        encoding="UTF-8",
        format="%(asctime)s %(levelname)s: %(message)s",
    )


@lru_cache(1)
def init_client():
    return AsyncClient(
        base_url="http://localhost:8000",
    )
