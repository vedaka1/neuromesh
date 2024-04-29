import uuid
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.neural_networks.model import Model
from domain.neural_networks.repository import BaseNeuralNetworkRepository


@dataclass
class NeuralNetworkRepository(BaseNeuralNetworkRepository):

    __slots__ = ("session",)
    session_factory: async_sessionmaker

    async def create(self, model: Model) -> None:
        async with self.session_factory() as session:
            query = text(
                """
                INSERT INTO neural_networks (id, name)
                VALUES (:id, :name);
                """
            )
            await session.execute(
                query,
                {
                    "id": model.id,
                    "name": model.name,
                },
            )
            await session.commit()
            return None

    async def delete(self, id: uuid.UUID) -> None:
        async with self.session_factory() as session:
            query = text(
                """
                DELETE FROM neural_networks
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

    async def get_by_id(self, id: uuid.UUID) -> Model:
        async with self.session_factory() as session:
            query = text("""SELECT * FROM neural_networks WHERE id = :value;""")
            result = await session.execute(query, {"value": id})
            result = result.mappings().one_or_none()
            if result is None:
                return None

            return Model(**result)

    async def get_by_name(self, name: str) -> Model:
        async with self.session_factory() as session:
            query = text("""SELECT * FROM neural_networks WHERE name = :name;""")
            result = await session.execute(query, {"name": name})
            result = result.mappings().one_or_none()
            if result is None:
                return None

            return Model(**result)

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Model]:
        async with self.session_factory() as session:
            query = text(
                """SELECT * FROM neural_networks LIMIT :limit OFFSET :offset;"""
            )
            result = await session.execute(query, {"limit": limit, "offset": offset})
            result = result.mappings().all()
            return [Model(**data) for data in result]

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
