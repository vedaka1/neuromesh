import uuid

from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.models.base import Base


class UserModelDB(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    telegram_id: Mapped[str] = mapped_column(nullable=False, index=True)
    username: Mapped[str] = mapped_column(nullable=True)
    current_subscription: Mapped[str] = mapped_column(nullable=True)
