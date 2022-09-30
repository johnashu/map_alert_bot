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

DATABASE_URL = os.getenv("DATABASE_URL", "my_precious1")  # os.environ["POSTGRES_DB"]

log = start_logger(verbose=verbose)

version = "1.0.0"
