import asyncio
from db.connection import DbConnect
from includes.config import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

# async def database(method, *a, **kw):
#     # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     db = DbConnect(POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)
#     task = asyncio.create_task(db.get_connection(method=method, *a, **kw))
#     await task


async def database(self, method, *a, **kw):
    db = DbConnect(POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)
    await self.get_connection(method=method, *a, **kw)
