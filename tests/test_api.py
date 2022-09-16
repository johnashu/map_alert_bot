import requests
import curlify
import logging, json

logging.basicConfig(level=logging.INFO, format="[%(levelname)s]: %(message)s")


def create_mismatch_address(l: list) -> list:
    """Replace Last Letter of the addresses to create a mismatch

    Args:
        l (list): list of addresses to change

    Returns:
        list: list of changed addresses
    """
    rtn = []
    for x in l:
        x = x[:-1] + "a"
        rtn.append(x)
    return rtn


def make_request(params: dict, url: str, route: str, headers: list = None) -> list:
    res = requests.post(url + route, params=params, headers=headers)

    logging.info(f"RES  ::  {res}  ::  {res.json()}\n\n")
    # logging.info(f"cURL Request:\n{curlify.to_curl(res.request)}\n")
    return res.json()


def base(
    params: tuple, expected: str, status: str = None, mismatch: bool = False, **kw
) -> None:
    for p in params:
        r = make_request(p, **kw)
        exp_res = r[0].get(expected)
        assert exp_res, f"Expected: {exp_res} | Got: {status}"
        if status:
            assert exp_res == status, f"Expected: {exp_res} | Got: {status}"
        # for idx, x in enumerate(r):
        #     if x.get("status") == "success":
        #         assert (
        #             address == x["owner_address"]
        #         ), f"Expected: {address} | Got: {x['address']}"

        #     elif mismatch:
        #         assert address != x["owner_address"]


def test_create_token(**kw) -> None:
    base((create_token,), "status", status="success", **kw)


if __name__ == "__main__":
    # Simple test script - execute when the app is running
    url = "http://127.0.0.1:5000"
    create_token = "/create_token/"
    register = "/register_address/"

    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NDk2NDIzNDgsImlhdCI6MTY2MzMyODc0Mywic3ViIjoibWFmZmF6In0.kFSH1lMvKHTvd7Kn8C5COzis90IfPIQHnlpAQw1qyUk"
    headers = {"api-token": token}

    kw = dict(url=url, route=create_token, headers=headers)
    kw = dict(url=url, route=register, headers=headers)

    # # test request
    params = ({"user_id": "maffaz"},)

    import datetime

    num_req = 1
    st = datetime.datetime.now()
    for _ in range(num_req):
        make_request(json.dumps(params), **kw)
    et = datetime.datetime.now()
    logging.info(f"Time ::  {et-st} for {num_req} calls")

    # # manual check tests. - uncomment to run.
    # test_create_token(**kw)
