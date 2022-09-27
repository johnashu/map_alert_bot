from urllib import response
import requests
import curlify
import logging, json
import datetime
from includes.config import BASE_URL, envs


logging.basicConfig(level=logging.INFO, format="[%(levelname)s]: %(message)s")


def make_request(params: dict, url: str, route: str, headers: list = None) -> list:
    res = requests.post(url + route, params=params, headers=headers)
    logging.info(f"\n{res}  ::  {res.json()}\n\n")
    logging.info(f"cURL Request:\n{curlify.to_curl(res.request)}\n")
    return res.json()


def get_map_data(
    route: str, url: str = BASE_URL, token: str = None, params: list = []
) -> tuple:

    # new_token = "/new_token/"
    # register = "/register_address/"

    headers = {"api-token": envs.ALERT_API_TOKEN}

    kw = dict(url=url, route=route, headers=headers)

    params = json.dumps(params)
    print(params)

    st = datetime.datetime.now()
    response = make_request(params, **kw)
    et = datetime.datetime.now()
    taken = et - st
    logging.info(
        f"Time ::  {taken}s\n\nRequests Per Sec  ::  {taken.total_seconds()}\n"
    )

    return True, response
