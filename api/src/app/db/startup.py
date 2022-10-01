import asyncio
from includes.config import DATABASE_URL
from db.connection import DbConnect

# DATABASE_URL = 'postgresql://maffaz:password@127.0.0.1/alertsDb'


def database(method, *a, **kw):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    db = DbConnect()  # POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)
    asyncio.run(db.get_connection(method=method, *a, DATABASE_URL=DATABASE_URL, **kw))


create_data = {
    "user_id": "serial PRIMARY KEY",
    "update_id": "serial",
    "chat_id": "serial",
    "first_name": "TEXT",
    "username": "TEXT",
    "text": "TEXT",
    "message_id": "INT",
    "date": "DATE",
    "language_code": "TEXT",
    "is_bot": "BOOLEAN",
    "pub_key": "TEXT",
    "is_validator": "BOOLEAN",
}

table_name = "users"
database("create_table", create_data, table=table_name)
