from dataclasses import dataclass

from asyncpg import Connection

from domain.users.repository import BaseUserRepository
from domain.users.user import User, UserDB


@dataclass(slots=True)
class UserRepository(BaseUserRepository):

    __slots__ = ("connection",)
    connection: Connection

    async def create(self, user: UserDB) -> None:
        async with self.connection.transaction():
            await self.connection.execute(
                """
                INSERT INTO users (id, telegram_id, username, is_premium)
                VALUES ($1, $2, $3, $4)
                """,
                user.id,
                user.telegram_id,
                user.username,
                user.is_premium,
            )
            return

    async def delete(self, telegram_id: int) -> None:
        async with self.connection.transaction():
            await self.connection.execute(
                """
                DELETE FROM users
                WHERE telegram_id = $1
                """,
                telegram_id,
            )
            return

    async def get_by_telegram_id(self, telegram_id: int) -> User:
        async with self.connection.transaction():
            self.connection.execute(
                "SELECT * FROM users WHERE telegram_id = $1", telegram_id
            )
            result = await self.connection.fetchrow()
        return result

    async def update_subscription(self, telegram_id: int, subscription: str):
        async with self.connection.transaction():
            await self.connection.execute(
                """
                UPDATE users
                SET subscription = $1
                WHERE telegram_id = $2
                """,
                subscription,
                telegram_id,
            )
            return
