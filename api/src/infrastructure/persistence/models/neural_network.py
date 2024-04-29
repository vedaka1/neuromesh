import uuid

from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.models.base import Base


class NeuralNetworkModelDB(Base):
    __tablename__ = "neural_networks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
