from dataclasses import dataclass

from domain.neural_networks.model import Model
from domain.neural_networks.repository import BaseNeuralNetworkRepository
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class NeuralNetworkRepository(BaseNeuralNetworkRepository):

    __slots__ = ("session",)
    session: AsyncSession

    async def create(self, model: Model) -> None:
        query = text(
            """
                INSERT INTO neural_networks (name)
                VALUES (:name);
                """
        )
        await self.session.execute(
            query,
            {
                "name": model.name,
            },
        )
        return None

    async def delete(self, name: str) -> None:
        query = text(
            """
                DELETE FROM neural_networks
                WHERE name = :value;
                """
        )
        await self.session.execute(
            query,
            {
                "value": name,
            },
        )

        return None

    async def get_by_name(self, name: str) -> Model:
        query = text("""SELECT * FROM neural_networks WHERE name = :value;""")
        result = await self.session.execute(query, {"value": name})
        result = result.mappings().one_or_none()
        if result is None:
            return None

        return Model(**result)

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Model]:
        query = text("""SELECT * FROM neural_networks LIMIT :limit OFFSET :offset;""")
        result = await self.session.execute(query, {"limit": limit, "offset": offset})
        result = result.mappings().all()
        return [Model(**data) for data in result]

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
