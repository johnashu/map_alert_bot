import psycopg
import asyncio
import logging


class DbConnect:
    async def get_connection(
        self,
        *a,
        DATABASE_URL: str = None,
        table: str = "test",
        method: str = "select",
        **kw,
    ):
        self.table = table
        async with await psycopg.AsyncConnection.connect(DATABASE_URL) as self.aconn:
            logging.info(DATABASE_URL)
            async with self.aconn.cursor() as self.acur:
                await self.__getattribute__(method)(*a, **kw)

    async def create_table(self, vals: dict):
        try:
            cols = self.dict_to_str(vals)[0:-1]
            SQL = f"""
                        CREATE TABLE {self.table} (                       
                            {cols.replace('=', '').replace("'", '')}
                            )
                """
            return await self.handle_result(await self.acur.execute(SQL), SQL)
        except psycopg.errors.DuplicateTable as e:
            logging.error(e)
            return False, e

    async def insert(self, vals: dict):
        cols, vals, _str = self.list_to_str(vals)
        SQL = f"INSERT INTO {self.table} {cols} VALUES {_str}"
        try:
            return await self.handle_result(await self.acur.execute(SQL, vals), SQL)
        except psycopg.errors.UniqueViolation as e:
            logging.error(e)

    async def update(self, vals: dict, condition="id = 1"):
        set_str = self.dict_to_str(vals)
        SQL = f"UPDATE {self.table} SET {set_str} WHERE {condition}"
        try:
            return await self.handle_result(await self.acur.execute(SQL), SQL)
        except psycopg.errors.UndefinedColumn as e:
            logging.error(e)

    async def select(self, fetch: int = 2, **kw):
        # fetchone = 1, fetchmany = 2 fetchall = 3
        fetches = {1: "fetchone", 2: "fetchmany", 3: "fetchall"}

        SQL = f"SELECT * FROM {self.table}"

        await self.acur.execute(SQL)
        get = self.acur.__getattribute__(fetches[fetch])
        results = await get(**kw)
        logging.info(results)
        for record in results:
            logging.info(f"{fetches[fetch].__repr__()}: {record}")

    @staticmethod
    async def handle_result(res, SQL) -> None:
        logging.info(f"Command Executed:\n\n\t{SQL}")
        if res:
            logging.info(f"Result:\n{res}")  # __str__())

    @staticmethod
    def list_to_str(vals: dict) -> tuple:
        if not vals:
            return "", [], ""

        def _list_to_str(vals: list) -> str:
            vals_str = "("
            if len(vals) > 1:
                for v in vals[:-1]:
                    vals_str += f"{v},"
            vals_str += f"{vals[-1]})"
            return vals_str

        cols = _list_to_str(list(vals.keys()))
        vals = list(vals.values())
        _str = _list_to_str(["%s"] * len(vals))
        return cols, vals, _str

    @staticmethod
    def dict_to_str(vals: dict) -> str:
        if not vals:
            return ""
        vals_str = ""
        keys = list(vals.keys())
        l = keys[-1]
        if len(keys) > 1:
            for x in keys[:-1]:
                vals_str += f"""{x} = '{vals[x]}', """
        vals_str += f"""{l} = '{vals[l]}'"""
        return vals_str


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    db = DbConnect()
    asyncio.run(db.get_connection())
