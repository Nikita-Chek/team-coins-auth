from decouple import config
from fastapi import HTTPException
from asyncpg import Connection, create_pool


class Database:
    def __init__(self):
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.host = config('DB_HOST')
        self.port = config('DB_PORT')
        self.database = config('DB_DATABASE')
        self._cursor = None
        self._connection_pool = None
        self.connection = None

    async def connect(self):
        if not self._connection_pool:
            try:
                self._connection_pool = await create_pool(
                    min_size=1,
                    max_size=10,
                    command_timeout=60,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    async def disconnect(self):
        if self._connection_pool:
            await self._connection_pool.close()

    def error_handler(func: callable):
        async def wrapped(self, *args, **kwargs):
            if not self._connection_pool:
                await self.connect()
            async with self._connection_pool.acquire() as conn:
                try:
                    result = await func(self, conn, *args, **kwargs)
                    return result
                except Exception as e:
                    raise e
        return wrapped

    @error_handler
    async def fetchrow(self, conn: Connection, query, *args, **kwargs):
        return await conn.fetchrow(query, *args, **kwargs)

    @error_handler
    async def fetchall(self, conn: Connection, query, *args, **kwargs):
        return await conn.fetch(query, *args, **kwargs)

    @error_handler
    async def fetchval(self, conn: Connection, query, *args, **kwargs):
        return await conn.fetchval(query, *args, **kwargs)

    @error_handler
    async def execute(self, conn: Connection, query, *args, **kwargs):
        return await conn.execute(query, *args, **kwargs)
