import uuid

from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.main import Base


class SubscriptionModelDB(Base):
    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    chatgpt_amount: Mapped[int] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=True)
