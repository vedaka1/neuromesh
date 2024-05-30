import uuid
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.subscriptions.subscription import Subscription


@dataclass
class SubscriptionRepository(BaseSubscriptionRepository):

    __slots__ = ("session",)
    session_factory: async_sessionmaker

    async def create(self, subscription: Subscription) -> None:
        async with self.session_factory() as session:
            query = text(
                """
                INSERT INTO subscriptions (name)
                VALUES (:name);
                """
            )
            await session.execute(
                query,
                {
                    "name": subscription.name,
                },
            )
            await session.commit()
            return None

    async def delete(self, name: str) -> None:
        async with self.session_factory() as session:
            query = text(
                """
                DELETE FROM subscriptions
                WHERE name = :name;
                """
            )
            await session.execute(
                query,
                {
                    "name": name,
                },
            )
            await session.commit()
            return None

    async def get_by_name(self, name: str) -> Subscription:
        async with self.session_factory() as session:
            query = text("""SELECT * FROM subscriptions WHERE name = :name;""")
            result = await session.execute(query, {"name": name})
            result = result.mappings().one_or_none()
            if result is None:
                return None

            return Subscription(**result)

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Subscription]:
        async with self.session_factory() as session:
            query = text("""SELECT * FROM subscriptions LIMIT :limit OFFSET :offset;""")
            result = await session.execute(query, {"limit": limit, "offset": offset})
            result = result.mappings().all()
            return [Subscription(**data) for data in result]

    async def update(self, name: str):
        async with self.session_factory() as session:
            query = text(
                """
                UPDATE subscriptions
                SET name = :val
                WHERE id = :id;
                """
            )
            await session.execute(
                query,
                {
                    "val": name,
                    "id": name,
                },
            )
            await session.commit()
            return None
