from dataclasses import dataclass

from application.common.transaction import ICommiter
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class Commiter(ICommiter):
    session: AsyncSession

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def close(self) -> None:
        await self.session.close()
