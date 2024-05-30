import uuid

from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.models.base import Base


class SubscriptionModelDB(Base):
    __tablename__ = "subscriptions"

    name: Mapped[str] = mapped_column(primary_key=True, index=True)
