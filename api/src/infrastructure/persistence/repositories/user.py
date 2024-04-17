from dataclasses import dataclass

from asyncpg import Connection

from domain.users.repository import BaseUserRepository
from domain.users.user import User, UserDB


@dataclass
class UserRepository(BaseUserRepository):

    __slots__ = ("connection",)
    connection: Connection

    async def create(self, user: UserDB) -> None:
        async with self.connection as conn:
            conn: Connection
            await conn.execute(
                """
                    INSERT INTO users (telegram_id, username, is_premium)
                    VALUES ($1, $2, $3);
                    """,
                user.telegram_id,
                user.username,
                user.is_premium,
            )
            return

    async def delete(self, telegram_id: int) -> None:
        async with self.connection as conn:
            result = await conn.execute(
                """
                DELETE FROM users
                WHERE telegram_id = $1;
                """,
                telegram_id,
            )
            return result

    async def get_by_telegram_id(self, telegram_id: int) -> UserDB:
        async with self.connection as conn:
            result = await conn.fetchrow(
                """SELECT * FROM users WHERE telegram_id = $1;""", telegram_id
            )
            return result

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[UserDB]:
        async with self.connection as conn:
            result = await conn.fetch(
                """SELECT * FROM users LIMIT $1 OFFSET $2;""", limit, offset
            )
            return result

    async def update_subscription(self, telegram_id: int, subscription: bool):
        async with self.connection as conn:
            await conn.execute(
                """
                UPDATE users
                SET is_premium = $1
                WHERE telegram_id = $2;
                """,
                subscription,
                telegram_id,
            )
            return
