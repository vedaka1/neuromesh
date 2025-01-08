from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.models.base import Base


class NeuralNetworkModelDB(Base):
    __tablename__ = 'neural_networks'

    name: Mapped[str] = mapped_column(primary_key=True, index=True)
