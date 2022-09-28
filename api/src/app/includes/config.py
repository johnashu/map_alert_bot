from includes.setup._envs import Envs
from includes.setup._logging import start_logger
from includes.setup._paths import *

import sys

sys.dont_write_bytecode = True

verbose = True

envs = Envs(envFile="api.env")
# print(envs.SECRET_KEY)
SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
TG_API_KEY = os.getenv("TG_API_KEY", "my_precious1")
dbname = (os.environ["POSTGRES_DB"],)
user = (os.environ["POSTGRES_USER"],)
password = os.environ["POSTGRES_PASSWORD"]
log = start_logger(verbose=verbose)

version = "1.0.0"
