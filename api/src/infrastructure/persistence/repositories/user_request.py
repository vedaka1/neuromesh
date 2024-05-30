import uuid
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.users.repository import BaseUserRequestRepository
from domain.users.user import UserRequest


@dataclass
class UserRequestRepository(BaseUserRequestRepository):

    __slots__ = ("session",)
    session_factory: async_sessionmaker

    async def create(self, user_request: UserRequest) -> None:
        async with self.session_factory() as session:
            query = text(
                """
                INSERT INTO users_requests (id, user_id, neural_network_name, amount)
                VALUES (:id, :user_id, :neural_network_name, :amount);
                """
            )
            await session.execute(
                query,
                {
                    "id": user_request.id,
                    "user_id": user_request.user_id,
                    "neural_network_name": user_request.neural_network_name,
                    "amount": user_request.amount,
                },
            )
            await session.commit()
            return None

    async def delete_user_requests(self, user_id: uuid.UUID) -> None:
        async with self.session_factory() as session:
            query = text(
                """
                DELETE FROM users_requests
                WHERE user_id = :value;
                """
            )
            await session.execute(
                query,
                {
                    "value": user_id,
                },
            )
            await session.commit()
            return None

    async def get_by_id(
        self, id: uuid.UUID, limit: int = 10, offset: int = 0
    ) -> list[UserRequest]:
        async with self.session_factory() as session:
            query = text(
                """SELECT * FROM users_requests WHERE id = :val LIMIT :limit OFFSET :offset;"""
            )
            result = await session.execute(
                query, {"val": id, "limit": limit, "offset": offset}
            )
            result = result.mappings().all()
            return [UserRequest(**data) for data in result]

    async def get_by_user_and_model_name(
        self, model_name: uuid.UUID, user_id: uuid.UUID
    ) -> UserRequest:
        async with self.session_factory() as session:
            query = text(
                """SELECT * FROM users_requests WHERE user_id = :user_id AND neural_network_name = :model_name;"""
            )
            result = await session.execute(
                query, {"user_id": user_id, "model_name": model_name}
            )
            result = result.mappings().one_or_none()
            if result is None:
                return None

            return UserRequest(**result)

    async def get_all_by_user_id(
        self, user_id: uuid.UUID, limit: int = 10, offset: int = 0
    ) -> list[UserRequest]:
        async with self.session_factory() as session:
            query = text(
                """SELECT * FROM users_requests WHERE user_id = :user_id LIMIT :limit OFFSET :offset;"""
            )
            result = await session.execute(
                query, {"user_id": user_id, "limit": limit, "offset": offset}
            )
            result = result.mappings().all()
            return [UserRequest(**data) for data in result]

    async def update_user_requests(
        self, user_id: uuid.UUID, model_name: str, amount: int
    ):
        async with self.session_factory() as session:
            query = text(
                """
                UPDATE users_requests
                SET amount = :val
                WHERE user_id = :id AND neural_network_name = :model_name;
                """
            )
            await session.execute(
                query,
                {
                    "val": amount,
                    "id": user_id,
                    "model_name": model_name,
                },
            )
            await session.commit()
            return None
