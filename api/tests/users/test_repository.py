import uuid

import pytest
from punq import Container

from src.domain.users.repository import BaseUserRepository
from src.domain.users.user import UserDB
from src.infrastructure.persistence.repositories.user import UserRepository


@pytest.mark.asyncio
class TestUserRepository:
    async def test_create_user(self, container: Container):
        user_repository = container.resolve(BaseUserRepository)
        # Create user
        user = UserDB.create(1, "test1")
        await user_repository.create(user)
        # Check it
        result = await user_repository.get_by_telegram_id(1)
        assert result["telegram_id"] == 1
        assert result["username"] == "test1"
        assert result["subscription"] is None
        # Delete user
        await user_repository.delete(1)

    async def test_delete_user(self, container: Container):
        user_repository = container.resolve(BaseUserRepository)
        # Create user
        user = UserDB.create(1, "test1")
        await user_repository.create(user)
        # Delete user
        await user_repository.delete(1)
        # Check it
        result = await user_repository.get_by_telegram_id(1)
        assert result is None

    # @pytest.mark.asyncio
    async def test_get_user_by_telegram_id(self, container: Container):
        user_repository = container.resolve(BaseUserRepository)
        # Create user
        user = UserDB.create(1, "test1")
        await user_repository.create(user)
        # Check it and get it
        result = await user_repository.get_by_telegram_id(1)
        assert result["telegram_id"] == 1
        # Delete user
        await user_repository.delete(1)

    async def test_get_all(self, container: Container):
        user_repository = container.resolve(BaseUserRepository)
        # Create users
        count = 2
        for i in range(count):
            user = UserDB.create(i, f"test{i}")
            await user_repository.create(user)
        # Check users
        result = await user_repository.get_all()
        assert len(result) == count
        # Delete users
        for user in result:
            await user_repository.delete(user["telegram_id"])

        result = await user_repository.get_all()
        assert len(result) == 0

    async def test_update_subscription(self, container: Container):
        user_repository: UserRepository = container.resolve(BaseUserRepository)
        # Create user
        user = UserDB.create(1, f"test1")
        await user_repository.create(user)
        # Check it and get it
        result = await user_repository.get_by_telegram_id(1)
        print(result)
        assert result["subscription"] is None
        # Update subscription
        id = uuid.uuid4()
        await user_repository.update_subscription(1, id)
        # Check suubscription
        result = await user_repository.get_by_telegram_id(1)
        assert str(result["subscription"]) == str(id)
        # Delete user
        await user_repository.delete(1)
