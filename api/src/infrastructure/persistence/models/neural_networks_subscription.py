import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.models.base import Base


class NeuralNetworksSubscriptionModelDB(Base):
    __tablename__ = "neural_networks_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    neural_network_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("neural_networks.id", ondelete="CASCADE")
    )
    subscription_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("subscriptions.id", ondelete="CASCADE")
    )
    requests: Mapped[int]
