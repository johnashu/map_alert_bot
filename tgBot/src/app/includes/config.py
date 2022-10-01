# t.me/MapAlertsBot
#
# By Maffaz 2022 - maffaz
#
from includes.setup._envs import Envs
from includes.setup._logging import start_logger
from includes.setup._paths import *

import sys

sys.dont_write_bytecode = True

verbose = True

envs = Envs(envFile=".env")
log = start_logger(verbose=verbose)


TG_API_KEY = os.getenv("TG_API_KEY", "Not Found a TG_API_KEY..")
ALERT_API_TOKEN = os.getenv("ALERT_API_TOKEN", "Not Found a ALERT_API_TOKEN..")
ALERT_API_BASE_URL = os.getenv("ALERT_API_BASE_URL", "Not Found a ALERT_API_BASE_URL..")
IS_DOCKER = os.getenv("IS_DOCKER", False)

if not IS_DOCKER:
    ALERT_API_BASE_URL = "http://127.0.0.1:8000/"


version = "1.0.0"

bot_name = "Map Alerts Bot"

help_msg_file = "help.txt"
start_msg_file = "start.txt"


links = dict(
    buy_link="https://maplabs.io",
    stake_map_video="https://youtu.be/Qvxm4tsN--0",
    stake_map_medium="https://medium.com/marcopolo-protocol/map-token-staking-tutorial-d78fc60e76e9",
    create_validator_medium="https://medium.com/marcopolo-protocol/a-step-by-step-guide-for-creating-a-validator-on-map-protocol-ab8ad14fae8f",
    twitter_address="https://twitter.com/MaffazO",
    telegram_address="https://t.me/MaffazO",
)

watermark = f"\n\n{links['buy_link']}"

# command:method_name
MENU_ITEMS = {
    # Admin
    "help": "help",
    "start": "start",
    "error": "error",
    # Endpoints
    "new_token": "handle_endpoints",
    "delete_token": "handle_endpoints",
    "register": "handle_endpoints",
    "validator_summary": "handle_endpoints",
}
