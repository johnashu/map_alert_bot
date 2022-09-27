from includes.setup._envs import Envs
from includes.setup._logging import start_logger
from includes.setup._paths import *

import sys

sys.dont_write_bytecode = True

verbose = True

envs = Envs(envFile="api.env")
SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
log = start_logger(verbose=verbose)

version = "1.0.0"
