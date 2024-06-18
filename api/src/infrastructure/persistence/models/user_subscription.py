import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.models.base import Base


class UserSubscriptionModelDB(Base):
    __tablename__ = "users_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    subscription_name: Mapped[str] = mapped_column(
        ForeignKey("subscriptions.name", ondelete="CASCADE")
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=func.now(),
        nullable=False,
    )
    expires_in: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=False,
    )
    is_expired: Mapped[bool] = mapped_column(nullable=False)
