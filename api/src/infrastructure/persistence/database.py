import asyncpg


class ConnectionContextManager:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool = pool

    async def __aenter__(self) -> asyncpg.Connection:
        self.connection = await self.pool.acquire()
        self.transaction = self.connection.transaction()
        await self.transaction.start()

        return self.connection

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            await self.transaction.rollback()
        else:
            await self.transaction.commit()

        await self.pool.release(self.connection)


class ConnectionPoolManager:
    def __init__(self, db_url: str) -> None:
        self.db_url = db_url
        self._pool_min_size = 10
        self._pool_max_size = 10
        self._pool = None

    async def _create_pool(self) -> None:
        self._pool = await asyncpg.create_pool(
            self.db_url,
            min_size=self._pool_min_size,
            max_size=self._pool_max_size,
        )

    async def get_connection(self) -> ConnectionContextManager:
        if self._pool is None:
            try:
                await self._create_pool()
            except:
                raise Exception("Failed to create connection pool")

        return ConnectionContextManager(self._pool)
