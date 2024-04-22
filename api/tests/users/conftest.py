import pytest

from src.domain.users.repository import BaseUserRepository


@pytest.fixture(scope="function")
def user_repository(container):
    user_reposutory = container.resolve(BaseUserRepository)
    yield user_reposutory
