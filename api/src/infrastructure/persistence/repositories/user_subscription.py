import uuid
from dataclasses import dataclass

from domain.users.repository import BaseUserSubscriptionRepository
from domain.users.user import UserSubscription
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class UserSubscriptionRepository(BaseUserSubscriptionRepository):
    __slots__ = ('session',)
    session: AsyncSession

    async def create(self, user_subscription: UserSubscription) -> None:
        query = text(
            """
            INSERT INTO users_subscriptions (id, user_id, subscription_name, expires_in, is_expired)
            VALUES (:id, :user_id, :subscription_name, :expires_in, :is_expired);
            """
        )
        await self.session.execute(
            query,
            {
                'id': user_subscription.id,
                'user_id': user_subscription.user_id,
                'subscription_name': user_subscription.subscription_name,
                'expires_in': user_subscription.expires_in,
                'is_expired': user_subscription.is_expired,
            },
        )

    async def delete(self, id: uuid.UUID) -> None:
        query = text(
            """
            DELETE FROM users_subscriptions
            WHERE id = :value;
            """
        )
        await self.session.execute(query, {'value': id})

    async def get_by_id(self, id: uuid.UUID) -> UserSubscription | None:
        query = text("""SELECT * FROM users_subscriptions WHERE id = :value;""")
        result = await self.session.execute(query, {'value': id})
        data = result.mappings().one_or_none()
        if not data:
            return None

        return UserSubscription(**data)

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[UserSubscription]:
        query = text("""SELECT * FROM users_subscriptions LIMIT :limit OFFSET :offset;""")
        result = await self.session.execute(query, {'limit': limit, 'offset': offset})
        data = result.mappings().all()
        return [UserSubscription(**item) for item in data]

    async def get_by_user_id(self, user_id: uuid.UUID, limit: int = 10, offset: int = 0) -> list[UserSubscription]:
        query = text("""SELECT * FROM users_subscriptions WHERE user_id = :user_id LIMIT :limit OFFSET :offset;""")
        result = await self.session.execute(query, {'user_id': user_id, 'limit': limit, 'offset': offset})
        data = result.mappings().all()
        return [UserSubscription(**item) for item in data]

    async def get_active_by_user_id(self, user_id: uuid.UUID):
        query = text("""SELECT * FROM users_subscriptions WHERE user_id = :user_id AND is_expired = false;""")
        result = await self.session.execute(query, {'user_id': user_id})
        data = result.mappings().one_or_none()
        if not data:
            return None

        return UserSubscription(**data)

    async def update(self, id: uuid.UUID) -> None:
        query = text(
            """
            UPDATE users_subscriptions
            SET is_expired = true
            WHERE id = :id;
            """
        )
        await self.session.execute(query, {'id': id})
