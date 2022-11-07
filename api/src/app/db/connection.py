from os import remove
import psycopg
from includes.config import DATABASE_URL, log, create_data


class DbConnect:
    def __init__(self, **kw) -> None:
        super(DbConnect, self).__init__(**kw)

    async def get_connection(
        self,
        *a,
        DATABASE_URL: str = None,
        table: str = "users",
        method: str = "create_table",
        **kw,
    ):
        self.table = table
        async with await psycopg.AsyncConnection.connect(DATABASE_URL) as self.aconn:
            log.info(DATABASE_URL)
            async with self.aconn.cursor() as self.acur:
                try:
                    await self.__getattribute__(method)(*a, **kw)
                except psycopg.errors.UndefinedColumn as e:
                    log.info(f"Cannot find Table, Creating New table..")
                    await self.create_table(create_data)

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
            log.error(e)
            return False, e

    async def insert(self, vals: dict):
        cols, vals, _str = self.list_to_str(vals)
        SQL = f"INSERT INTO {self.table} {cols} VALUES {_str}"
        try:
            res = await self.acur.execute(SQL, vals)
            return True, await self.handle_result(res, SQL, log.info)
        except psycopg.errors.UniqueViolation as e:
            return False, await self.handle_result(e, SQL, log.error)

    async def update(self, vals: dict, condition="id = 1"):
        set_str = self.dict_to_str(vals)
        SQL = f"UPDATE {self.table} SET {set_str} WHERE {condition}"
        try:
            return await self.handle_result(await self.acur.execute(SQL), SQL)
        except psycopg.errors.UndefinedColumn as e:
            log.error(e)

    async def select(self, fetch: int = 2, where: str = False, **kw):
        # fetchone = 1, fetchmany = 2 fetchall = 3
        fetches = {1: "fetchone", 2: "fetchmany", 3: "fetchall"}

        WHERE = f"WHERE {where}"

        if not where:
            WHERE = ""

        SQL = f"SELECT * FROM {self.table} {WHERE}"

        await self.acur.execute(SQL)
        get = self.acur.__getattribute__(fetches[fetch])
        results = await get(**kw)
        for record in results:
            log.info(f"{fetches[fetch].__repr__()}: {record}")
        return False

    @staticmethod
    async def handle_result(res, SQL: str, level=log.info) -> None:
        level(f"Command Executed:\n\n\t{SQL}")
        if res:
            level(f"Result:\n{res}")  # __str__())

    @staticmethod
    def list_to_str(vals: dict) -> tuple:
        if not vals:
            return "", [], ""

        vals = {k: v for k, v in vals.items() if k != "value"}

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
        vals = {k: v for k, v in vals.items() if k != "value"}
        vals_str = ""
        keys = list(vals.keys())
        l = keys[-1]
        if len(keys) > 1:
            for x in keys[:-1]:
                vals_str += f"""{x} = '{vals[x]}', """
        vals_str += f"""{l} = '{vals[l]}'"""
        return vals_str
