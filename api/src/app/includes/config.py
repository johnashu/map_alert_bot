from includes.setup._envs import Envs
from includes.setup._logging import start_logger
from includes.setup._paths import *

import sys

sys.dont_write_bytecode = True

verbose = True

envs = Envs(envFile=".env")
# print(envs.SECRET_KEY)
SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
TG_API_KEY = os.getenv("TG_API_KEY", "my_precious1")

POSTGRES_DB = os.getenv("POSTGRES_DB", "my_precious1")  # os.environ["POSTGRES_DB"]
POSTGRES_USER = os.getenv(
    "POSTGRES_USER", "my_precious1"
)  # os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD", "my_precious1"
)  # os.environ["POSTGRES_PASSWORD"]
log = start_logger(verbose=verbose)

version = "1.0.0"
