from includes.config import envs
import uvicorn
import urllib.parse, json
import logging
from includes.messages import *
from users.tokens import encode_auth_token, decode_auth_token
from routes.routes import routes


async def create_token(send, params: str) -> None:
    user_id = params[0].get("user_id")
    if not user_id:
        body = [{"error": bad_request_msg}]
        await send_response(send, body, status=400)
    else:
        res, token = await encode_auth_token(user_id)
        if res:
            return await send_response(send, {"api-token": token}, status=200)
        return await send_response(
            send, {"Error": token_gen_failed, "msg": str(token)}, status=501
        )


async def check_auth_token(send, token: str) -> bool:
    valid_token, user_id, msg = await decode_auth_token(token)
    if valid_token:
        return True
    else:
        body = [{"error": token_refused, "msg": msg}]
        await send_response(send, body, status=401)
        return False


async def parse_request(send, route: str, q: str) -> bool:
    if not q:
        body = [{"error": empty_msg}]
        return False, await send_response(send, body, status=400)

    dec = urllib.parse.unquote(q.decode())
    params = json.loads(dec)
    logging.info(params)

    if route == "/create_token/":
        await create_token(send, params)
        return True, params
    return False, params


async def send_response(send, body: list, status: int = 200):
    await send(dict(http_response_start, **{"status": status}))
    body = json.dumps(body).encode("utf-8")
    await send(dict(http_response_body, **{"body": body}))


async def app(scope, receive, send):
    #     routes = {
    #     '/register_address/': register_address,
    # }
    assert scope["type"] == "http"
    q = scope["query_string"]
    h = scope["headers"]
    route = scope["path"]
    logging.info(route)

    is_new_token, params = await parse_request(send, route, q)
    if not is_new_token:
        token = dict((x, y) for x, y in h).get(b"api-token").decode()
        logging.info(f"token: {token}  ::  params: {params}")
        is_authorised = await check_auth_token(send, token)
        if is_authorised:
            await routes[route](send, params, send_response)


if __name__ == "__main__":

    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)
