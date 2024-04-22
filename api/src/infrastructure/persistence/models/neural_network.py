import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.models.base import Base


class NeuralNetworkModelDB(Base):
    __tablename__ = "neural_networks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    subscription_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("subscriptions.id", ondelete="CASCADE")
    )
    name: Mapped[str]
    requests_amount: Mapped[int]
