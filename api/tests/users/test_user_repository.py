import pytest
from dishka import AsyncContainer

from domain.users.repository import BaseUserRepository
from domain.users.user import UserDB

pytestmark = pytest.mark.asyncio(scope="session")


class TestUserRepository:
    async def test_create_user(self, container: AsyncContainer):
        async with container() as di_container:
            user_repository = await di_container.get(BaseUserRepository)
            # Create user
            user = UserDB.create(1, "test1")
            await user_repository.create(user)
            # Check it
            user = await user_repository.get_by_telegram_id(1)
            assert user.telegram_id == 1
            assert user.username == "test1"
            assert user.current_subscription == "Free"
            # Delete user
            await user_repository.delete(1)

    async def test_delete_user(self, container: AsyncContainer):
        async with container() as di_container:
            user_repository = await di_container.get(BaseUserRepository)
            # Create user
            user = UserDB.create(1, "test1")
            await user_repository.create(user)
            # Delete user
            await user_repository.delete(1)
            # Check it
            result = await user_repository.get_by_telegram_id(1)
            assert result is None

    async def test_get_user_by_telegram_id(self, container: AsyncContainer):
        async with container() as di_container:
            user_repository = await di_container.get(BaseUserRepository)
            # Create user
            user = UserDB.create(1, "test1")
            await user_repository.create(user)
            # Check it and get it
            user = await user_repository.get_by_telegram_id(1)
            assert user.telegram_id == 1
            # Delete user
            await user_repository.delete(1)

    async def test_get_all_users(self, container: AsyncContainer):
        async with container() as di_container:
            user_repository = await di_container.get(BaseUserRepository)
            # Create users
            count = 2
            for i in range(count):
                user = UserDB.create(i, f"test{i}")
                await user_repository.create(user)
            # Check users
            users = await user_repository.get_all()
            assert len(users) == count
            # Delete users
            for user in users:
                await user_repository.delete(user.telegram_id)

            users = await user_repository.get_all()
            assert len(users) == 0

    # async def test_update_user_subscription(self, user_repository: UserRepository):
    #     user = UserDB.create(1, f"test1")  # Create user
    #     await user_repository.create(user)
    #     user = await user_repository.get_by_telegram_id(1)  # Check it and get it
    #     assert user.current_subscription_id == False

    #     id = uuid.uuid4()
    #     await user_repository.update_subscription(1, True)  # Update subscription
    #     user = await user_repository.get_by_telegram_id(1)  # Check subscription
    #     assert user.current_subscription_id == True

    #     await user_repository.delete(1)  # Delete user
