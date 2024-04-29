import uuid
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.users.repository import BaseUserRepository
from domain.users.user import User, UserDB


@dataclass
class UserRepository(BaseUserRepository):

    __slots__ = ("session",)
    session_factory: async_sessionmaker

    async def create(self, user: UserDB) -> None:
        async with self.session_factory() as session:
            query = text(
                """
                INSERT INTO users (id, telegram_id, username, current_subscription_id)
                VALUES (:id, :telegram_id, :username, :current_subscription_id);
                """
            )
            await session.execute(
                query,
                {
                    "id": user.id,
                    "telegram_id": user.telegram_id,
                    "username": user.username,
                    "current_subscription_id": user.current_subscription_id,
                },
            )
            await session.commit()
            return None

    async def delete(self, telegram_id: int) -> None:
        async with self.session_factory() as session:
            query = text(
                """
                DELETE FROM users
                WHERE telegram_id = :value;
                """
            )
            await session.execute(
                query,
                {
                    "value": telegram_id,
                },
            )
            await session.commit()
            return None

    async def get_by_telegram_id(self, telegram_id: int) -> UserDB:
        async with self.session_factory() as session:
            query = text("""SELECT * FROM users WHERE telegram_id = :value;""")
            result = await session.execute(query, {"value": telegram_id})
            result = result.mappings().one_or_none()
            if result is None:
                return None

            return UserDB(**result)

    async def get_by_id(self, user_id: uuid.UUID) -> UserDB:
        async with self.session_factory() as session:
            query = text("""SELECT * FROM users WHERE id = :value;""")
            result = await session.execute(query, {"value": user_id})
            result = result.mappings().one_or_none()
            if result is None:
                return None

            return UserDB(**result)

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[UserDB]:
        async with self.session_factory() as session:
            query = text("""SELECT * FROM users LIMIT :limit OFFSET :offset;""")
            result = await session.execute(query, {"limit": limit, "offset": offset})
            result = result.mappings().all()
            return [UserDB(**data) for data in result]

    async def update_subscription(self, user_id: uuid.UUID, subscription_id: uuid.UUID):
        async with self.session_factory() as session:
            query = text(
                """
                UPDATE users
                SET current_subscription_id = :val
                WHERE id = :id;
                """
            )
            await session.execute(
                query,
                {
                    "val": subscription_id,
                    "id": user_id,
                },
            )
            await session.commit()
            return None
