from includes.setup._envs import Envs
from includes.setup._logging import start_logger
from includes.setup._paths import *

import sys

sys.dont_write_bytecode = True

verbose = True

envs = Envs(envFile=".env")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "my_precious")
TG_API_KEY = os.getenv("TG_API_KEY", "my_precious1")
DATABASE_URL = os.getenv("DATABASE_URL", "my_precious1")

log = start_logger(verbose=verbose)

version = "1.0.0"

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
