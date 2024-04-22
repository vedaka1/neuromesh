from functools import lru_cache

from punq import Container, Scope
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.users.repository import BaseUserRepository
from infrastructure.persistence.main import (
    create_engine,
    create_session,
    create_session_factory,
)
from infrastructure.persistence.repositories.user import UserRepository


@lru_cache(1)
def get_container() -> Container:
    container = init_container()
    return container


def init_container() -> Container:
    container = Container()
    engine = create_engine()
    session_factory = create_session_factory(engine)
    container.register(
        async_sessionmaker, instance=session_factory, scope=Scope.singleton
    )

    container.register(
        BaseUserRepository,
        UserRepository,
        scope=Scope.transient,
    )
    return container
