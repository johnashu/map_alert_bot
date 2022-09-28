import psycopg
import asyncio
from api.src.app.includes.config import *


class DbConnect:
    async def get_connection(self):

        async with await psycopg.AsyncConnection.connect(
            dbname, user, password
        ) as aconn:
            print(aconn)
            async with aconn.cursor() as acur:
                print(acur)
                await acur.execute(
                    "INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def")
                )
                await acur.execute("SELECT * FROM test")
                await acur.fetchone()
                # will return (1, 100, "abc'def")
                async for record in acur:
                    print(record)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    db = DbConnect()
    asyncio.run(db.get_connection())
