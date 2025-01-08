import uuid
from dataclasses import dataclass

from domain.neural_networks.model import ModelSubscription
from domain.neural_networks.repository import BaseNeuralNetworkSubscriptionRepository
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class NeuralNetworkSubscriptionRepository(BaseNeuralNetworkSubscriptionRepository):
    __slots__ = ('session',)
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
                'id': model_subscription.id,
                'model_name': model_subscription.neural_network_name,
                'subscription_name': model_subscription.subscription_name,
                'requests': model_subscription.requests,
            },
        )
        await self.session.commit()

    async def delete(self, id: uuid.UUID) -> None:
        query = text(
            """
            DELETE FROM neural_networks_subscriptions
            WHERE id = :value;
            """
        )
        await self.session.execute(query, {'value': id})

    async def get_by_id(self, id: uuid.UUID) -> ModelSubscription | None:
        query = text("""SELECT * FROM neural_networks_subscriptions WHERE id = :value;""")
        result = await self.session.execute(query, {'value': id})
        data = result.mappings().one_or_none()
        if not data:
            return None

        return ModelSubscription(**data)

    async def get_by_subscription_and_model_name(
        self, subscription_name: str, model_name: str
    ) -> ModelSubscription | None:
        query = text(
            """
            SELECT * FROM neural_networks_subscriptions
            WHERE subscription_name = :sub_name AND neural_network_name = :model_name;
            """
        )
        result = await self.session.execute(query, {'sub_name': subscription_name, 'model_name': model_name})
        data = result.mappings().one_or_none()
        if not data:
            return None

        return ModelSubscription(**data)

    async def get_all_by_subscription_name(self, subscription_name: str) -> list[ModelSubscription]:
        query = text("""SELECT * FROM neural_networks_subscriptions WHERE subscription_name = :name;""")
        result = await self.session.execute(query, {'name': subscription_name})
        data = result.mappings().all()
        return [ModelSubscription(**item) for item in data]

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[ModelSubscription]:
        query = text("""SELECT * FROM neural_networks_subscriptions LIMIT :limit OFFSET :offset;""")
        result = await self.session.execute(query, {'limit': limit, 'offset': offset})
        data = result.mappings().all()
        return [ModelSubscription(**item) for item in data]

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
