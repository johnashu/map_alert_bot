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


BASE_URL = "http://api:8000/"
BASE_URL = "http://127.0.0.1:8000/"


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

ENDPOINTS = {
    "new_token": "new_token",
    "register": "register_address",
}
