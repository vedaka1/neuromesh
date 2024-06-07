import uuid
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.users.repository import BaseUserRepository
from domain.users.user import UserDB


@dataclass
class UserRepository(BaseUserRepository):

    __slots__ = ("session",)
    session: AsyncSession

    async def create(self, user: UserDB) -> None:
        query = text(
            """
                INSERT INTO users (id, telegram_id, username, current_subscription)
                VALUES (:id, :telegram_id, :username, :current_subscription);
                """
        )
        await self.session.execute(
            query,
            {
                "id": user.id,
                "telegram_id": user.telegram_id,
                "username": user.username,
                "current_subscription": user.current_subscription,
            },
        )
        return None

    async def delete(self, telegram_id: int) -> None:
        query = text(
            """
                DELETE FROM users
                WHERE telegram_id = :value;
                """
        )
        await self.session.execute(
            query,
            {
                "value": telegram_id,
            },
        )
        return None

    async def get_by_telegram_id(self, telegram_id: int) -> UserDB:
        query = text("""SELECT * FROM users WHERE telegram_id = :value;""")
        result = await self.session.execute(query, {"value": telegram_id})
        result = result.mappings().one_or_none()
        if result is None:
            return None

        return UserDB(**result)

    async def get_by_id(self, user_id: uuid.UUID) -> UserDB:
        query = text("""SELECT * FROM users WHERE id = :value;""")
        result = await self.session.execute(query, {"value": user_id})
        result = result.mappings().one_or_none()
        if result is None:
            return None

        return UserDB(**result)

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[UserDB]:
        query = text("""SELECT * FROM users LIMIT :limit OFFSET :offset;""")
        result = await self.session.execute(query, {"limit": limit, "offset": offset})
        result = result.mappings().all()
        return [UserDB(**data) for data in result]

    async def update_subscription(self, user_id: uuid.UUID, subscription_name: str):
        query = text(
            """
                UPDATE users
                SET current_subscription = :val
                WHERE id = :id;
                """
        )
        await self.session.execute(
            query,
            {
                "val": subscription_name,
                "id": user_id,
            },
        )
        return None
