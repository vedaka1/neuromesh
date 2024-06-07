import uuid
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.neural_networks.model import ModelSubscription
from domain.neural_networks.repository import BaseNeuralNetworkSubscriptionRepository


@dataclass
class NeuralNetworkSubscriptionRepository(BaseNeuralNetworkSubscriptionRepository):

    __slots__ = ("session",)
    session: AsyncSession

    async def create(self, model_subscription: ModelSubscription) -> None:
        query = text(
            """
                INSERT INTO neural_networks_subscriptions (id, subscription_name, neural_network_name, requests)
                VALUES (:id, :subscription_name, :model_name, :requests);
                """
        )
        await self.session.execute(
            query,
            {
                "id": model_subscription.id,
                "model_name": model_subscription.neural_network_name,
                "subscription_name": model_subscription.subscription_name,
                "requests": model_subscription.requests,
            },
        )
        await self.session.commit()
        return None

    async def delete(self, id: uuid.UUID) -> None:
        query = text(
            """
                DELETE FROM neural_networks_subscriptions
                WHERE id = :value;
                """
        )
        await self.session.execute(
            query,
            {
                "value": id,
            },
        )
        return None

    async def get_by_id(self, id: uuid.UUID) -> ModelSubscription:
        query = text(
            """SELECT * FROM neural_networks_subscriptions WHERE id = :value;"""
        )
        result = await self.session.execute(query, {"value": id})
        result = result.mappings().one_or_none()
        if result is None:
            return None

        return ModelSubscription(**result)

    async def get_all_by_subscription_name(
        self, subscription_name: uuid.UUID
    ) -> list[ModelSubscription]:
        query = text(
            """SELECT * FROM neural_networks_subscriptions WHERE subscription_name = :name;"""
        )
        result = await self.session.execute(query, {"name": subscription_name})
        result = result.mappings().all()
        if result is None:
            return None

        return [ModelSubscription(**data) for data in result]

    async def get_all(
        self, limit: int = 10, offset: int = 0
    ) -> list[ModelSubscription]:
        query = text(
            """SELECT * FROM neural_networks_subscriptions LIMIT :limit OFFSET :offset;"""
        )
        result = await self.session.execute(query, {"limit": limit, "offset": offset})
        result = result.mappings().all()
        return [ModelSubscription(**data) for data in result]

    # async def get_all_by_subscription_id(
    #     self, subscription_id: uuid.UUID, limit: int = 10, offset: int = 0
    # ) -> list[Model]:
    #
    #         query = text(
    #             """SELECT * FROM neural_networks_subscriptions WHERE subscription_id = :subscription_id LIMIT :limit OFFSET :offset;"""
    #         )
    #         result = await self.session.execute(
    #             query,
    #             {"subscription_id": subscription_id, "limit": limit, "offset": offset},
    #         )
    #         result = result.mappings().all()
    #         return [Model(**data) for data in result]
