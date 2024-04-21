import uuid
from dataclasses import dataclass

from asyncpg import Connection
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
                INSERT INTO users (id, telegram_id, username, subscription)
                VALUES (:id, :telegram_id, :username, :subscription);
                """
            )
            await session.execute(
                query,
                {
                    "id": user.id,
                    "telegram_id": user.telegram_id,
                    "username": user.username,
                    "subscription": user.subscripion,
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
            result = await session.execute(
                query,
                {
                    "value": telegram_id,
                },
            )
            await session.commit()
            return None

    async def get_by_telegram_id(self, telegram_id: int) -> UserDB:
        query = text("""SELECT * FROM users WHERE telegram_id = :value;""")
        async with self.session_factory() as session:
            result = await session.execute(query, {"value": telegram_id})
            return result.mappings().one_or_none()

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[UserDB]:
        async with self.session_factory() as session:
            query = text("""SELECT * FROM users LIMIT :limit OFFSET :offset;""")
            result = await session.execute(query, {"limit": limit, "offset": offset})
            return result.mappings().all()

    async def update_subscription(self, telegram_id: int, subscription: uuid.UUID):
        async with self.session_factory() as session:
            query = text(
                """
                UPDATE users
                SET subscription = :val
                WHERE telegram_id = :id;
                """
            )
            result = await session.execute(
                query,
                {
                    "val": subscription,
                    "id": telegram_id,
                },
            )
            await session.commit()
            return None
