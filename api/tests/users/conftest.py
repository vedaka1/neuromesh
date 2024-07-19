import pytest
from dishka import AsyncContainer

from domain.users.repository import BaseUserRepository

# @pytest.fixture(scope="function")
# @pytest.mark.asyncio
# async def user_repository(container: AsyncContainer):
#     async with container() as di_container:
#         user_repository = await di_container.get(BaseUserRepository)
#         yield user_repository
