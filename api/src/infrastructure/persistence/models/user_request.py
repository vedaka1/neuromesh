import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.models.base import Base


class UserRequestModelDB(Base):
    __tablename__ = 'users_requests'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    amount: Mapped[int]
    neural_network_name: Mapped[str] = mapped_column(ForeignKey('neural_networks.name', ondelete='CASCADE'))
