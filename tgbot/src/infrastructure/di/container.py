import logging
from functools import lru_cache

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
def init_client() -> AsyncClient:
    return AsyncClient(
        base_url="http://api:8000",
    )
