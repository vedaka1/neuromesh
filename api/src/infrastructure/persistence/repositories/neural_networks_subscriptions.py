import uuid
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.neural_networks.model import ModelSubscription
from domain.neural_networks.repository import BaseNeuralNetworkSubscriptionRepository


@dataclass
class NeuralNetworkSubscriptionRepository(BaseNeuralNetworkSubscriptionRepository):

    __slots__ = ("session",)
    session_factory: async_sessionmaker

    async def create(self, model_subscription: ModelSubscription) -> None:
        async with self.session_factory() as session:
            query = text(
                """
                INSERT INTO neural_networks_subscriptions (id, subscription_id, neural_network_id, requests)
                VALUES (:id, :subscription_id, :model_id, :requests);
                """
            )
            await session.execute(
                query,
                {
                    "id": model_subscription.id,
                    "model_id": model_subscription.neural_network_id,
                    "subscription_id": model_subscription.subscription_id,
                    "requests": model_subscription.requests,
                },
            )
            await session.commit()
            return None

    async def delete(self, id: uuid.UUID) -> None:
        async with self.session_factory() as session:
            query = text(
                """
                DELETE FROM neural_networks_subscriptions
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

    async def get_by_id(self, id: uuid.UUID) -> ModelSubscription:
        async with self.session_factory() as session:
            query = text(
                """SELECT * FROM neural_networks_subscriptions WHERE id = :value;"""
            )
            result = await session.execute(query, {"value": id})
            result = result.mappings().one_or_none()
            if result is None:
                return None

            return ModelSubscription(**result)

    async def get_all_by_subscription_id(
        self, subscription_id: uuid.UUID
    ) -> list[ModelSubscription]:
        async with self.session_factory() as session:
            query = text(
                """SELECT * FROM neural_networks_subscriptions WHERE subscription_id = :id;"""
            )
            result = await session.execute(query, {"id": subscription_id})
            result = result.mappings().all()
            if result is None:
                return None

            return [ModelSubscription(**data) for data in result]

    async def get_all(
        self, limit: int = 10, offset: int = 0
    ) -> list[ModelSubscription]:
        async with self.session_factory() as session:
            query = text(
                """SELECT * FROM neural_networks_subscriptions LIMIT :limit OFFSET :offset;"""
            )
            result = await session.execute(query, {"limit": limit, "offset": offset})
            result = result.mappings().all()
            return [ModelSubscription(**data) for data in result]

    # async def get_all_by_subscription_id(
    #     self, subscription_id: uuid.UUID, limit: int = 10, offset: int = 0
    # ) -> list[Model]:
    #     async with self.session_factory() as session:
    #         query = text(
    #             """SELECT * FROM neural_networks_subscriptions WHERE subscription_id = :subscription_id LIMIT :limit OFFSET :offset;"""
    #         )
    #         result = await session.execute(
    #             query,
    #             {"subscription_id": subscription_id, "limit": limit, "offset": offset},
    #         )
    #         result = result.mappings().all()
    #         return [Model(**data) for data in result]
