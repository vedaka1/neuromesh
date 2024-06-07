from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.subscriptions.repository import BaseSubscriptionRepository
from domain.subscriptions.subscription import Subscription


@dataclass
class SubscriptionRepository(BaseSubscriptionRepository):

    __slots__ = ("session",)
    session: AsyncSession

    async def create(self, subscription: Subscription) -> None:
        query = text(
            """
                INSERT INTO subscriptions (name)
                VALUES (:name);
                """
        )
        await self.session.execute(
            query,
            {
                "name": subscription.name,
            },
        )
        return None

    async def delete(self, name: str) -> None:
        query = text(
            """
                DELETE FROM subscriptions
                WHERE name = :name;
                """
        )
        await self.session.execute(
            query,
            {
                "name": name,
            },
        )
        return None

    async def get_by_name(self, name: str) -> Subscription:
        query = text("""SELECT * FROM subscriptions WHERE name = :name;""")
        result = await self.session.execute(query, {"name": name})
        result = result.mappings().one_or_none()
        if result is None:
            return None

        return Subscription(**result)

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Subscription]:
        query = text("""SELECT * FROM subscriptions LIMIT :limit OFFSET :offset;""")
        result = await self.session.execute(query, {"limit": limit, "offset": offset})
        result = result.mappings().all()
        return [Subscription(**data) for data in result]

    async def update(self, name: str):
        query = text(
            """
                UPDATE subscriptions
                SET name = :val
                WHERE id = :id;
                """
        )
        await self.session.execute(
            query,
            {
                "val": name,
                "id": name,
            },
        )
        return None
