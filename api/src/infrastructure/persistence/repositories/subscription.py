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
                INSERT INTO subscriptions (id, name, validity_period)
                VALUES (:id, :name, :validity_period);
                """
            )
            await session.execute(
                query,
                {
                    "id": subscription.id,
                    "name": subscription.name,
                    "validity_period": subscription.validity_period,
                },
            )
            await session.commit()
            return None

    async def delete(self, id: uuid.UUID) -> None:
        async with self.session_factory() as session:
            query = text(
                """
                DELETE FROM subscriptions
                WHERE id = :value;
                """
            )
            await session.execute(
                query,
                {
                    "value": id,
                },
            )
            await session.commit()
            return None

    async def get_by_id(self, id: uuid.UUID) -> Subscription:
        async with self.session_factory() as session:
            query = text("""SELECT * FROM subscriptions WHERE id = :value;""")
            result = await session.execute(query, {"value": id})
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

    async def update(self, id: uuid.UUID, validity_period: int):
        async with self.session_factory() as session:
            query = text(
                """
                UPDATE subscriptions
                SET validity_period = :val
                WHERE id = :id;
                """
            )
            await session.execute(
                query,
                {
                    "val": validity_period,
                    "id": id,
                },
            )
            await session.commit()
            return None
