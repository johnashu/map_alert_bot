import psycopg
import asyncio


class DbConnect:

    def __init__(self, dbname, user, password) -> None:
        self.dbname = dbname
        self.user = user
        self.password = password 

    async def get_connection(self, ):        

        async with await psycopg.AsyncConnection.connect(
            f"dbname={self.dbname} user={self.user} password={self.password}"
        ) as self.aconn:
            async with self.aconn.cursor() as self.acur:
                print(self.acur)
                await self.acur.execute(
                    "INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def")
                )
                await self.acur.execute("SELECT * FROM test")
                await self.acur.fetchone()
                # will return (1, 100, "abc'def")
                async for record in self.acur:
                    print(record)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    db = DbConnect()
    asyncio.run(db.get_connection())
