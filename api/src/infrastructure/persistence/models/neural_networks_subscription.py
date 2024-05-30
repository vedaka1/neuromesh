import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.models.base import Base


class NeuralNetworksSubscriptionModelDB(Base):
    __tablename__ = "neural_networks_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    neural_network_name: Mapped[str] = mapped_column(
        ForeignKey("neural_networks.name", ondelete="CASCADE")
    )
    subscription_name: Mapped[str] = mapped_column(
        ForeignKey("subscriptions.name", ondelete="CASCADE")
    )
    requests: Mapped[int]
