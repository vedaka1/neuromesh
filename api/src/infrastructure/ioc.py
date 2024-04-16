from functools import lru_cache

from punq import Container, Scope

from domain.users.repository import BaseUserRepository
from infrastructure.config import settings
from infrastructure.persistence.database import DatabaseResource
from infrastructure.persistence.repositories.user import UserRepository


@lru_cache(1)
def get_container() -> Container:
    container = init_container()
    return container


def init_container() -> Container:
    container = Container()

    container.register(
        DatabaseResource,
        instance=DatabaseResource(settings.DB_URL),
        scope=Scope.singleton,
    )

    async def init_user_repository() -> UserRepository:
        db: DatabaseResource = container.resolve(DatabaseResource)
        user_repository = UserRepository(connection=await db.get_connection())
        return user_repository

    container.register(
        BaseUserRepository, factory=init_user_repository, scope=Scope.transient
    )
    return container
