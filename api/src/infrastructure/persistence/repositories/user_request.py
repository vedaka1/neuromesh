import uuid
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.users.repository import BaseUserRequestRepository
from domain.users.user import UserRequest


@dataclass
class UserRequestRepository(BaseUserRequestRepository):

    __slots__ = ("session",)
    session: AsyncSession

    async def create(self, user_request: UserRequest) -> None:
        query = text(
            """
                INSERT INTO users_requests (id, user_id, neural_network_name, amount)
                VALUES (:id, :user_id, :neural_network_name, :amount);
                """
        )
        await self.session.execute(
            query,
            {
                "id": user_request.id,
                "user_id": user_request.user_id,
                "neural_network_name": user_request.neural_network_name,
                "amount": user_request.amount,
            },
        )
        return None

    async def delete_user_requests(self, user_id: uuid.UUID) -> None:
        query = text(
            """
                DELETE FROM users_requests
                WHERE user_id = :value;
                """
        )
        await self.session.execute(
            query,
            {
                "value": user_id,
            },
        )
        return None

    async def get_by_id(self, id: uuid.UUID) -> UserRequest | None:
        query = text("""SELECT * FROM users_requests WHERE id = :val""")
        result = await self.session.execute(query, {"val": id})
        data = result.mappings().all()
        if not data:
            return None
        return UserRequest(**data)

    async def get_by_user_and_model_name(
        self, model_name: str, user_id: uuid.UUID
    ) -> UserRequest | None:
        query = text(
            """SELECT * FROM users_requests WHERE user_id = :user_id AND neural_network_name = :model_name;"""
        )
        result = await self.session.execute(
            query, {"user_id": user_id, "model_name": model_name}
        )
        data = result.mappings().one_or_none()
        if data is None:
            return None

        return UserRequest(**data)

    async def get_all_by_user_id(
        self, user_id: uuid.UUID, limit: int = 10, offset: int = 0
    ) -> list[UserRequest]:
        query = text(
            """SELECT * FROM users_requests WHERE user_id = :user_id LIMIT :limit OFFSET :offset;"""
        )
        result = await self.session.execute(
            query, {"user_id": user_id, "limit": limit, "offset": offset}
        )
        data = result.mappings().all()
        return [UserRequest(**item) for item in data]

    async def update_user_requests(
        self, user_id: uuid.UUID, model_name: str, amount: int
    ):
        query = text(
            """
                UPDATE users_requests
                SET amount = :val
                WHERE user_id = :id AND neural_network_name = :model_name;
                """
        )
        await self.session.execute(
            query,
            {
                "val": amount,
                "id": user_id,
                "model_name": model_name,
            },
        )
        return None
