import uvicorn
import urllib.parse, json
import logging
from includes.messages import *
from users.tokens import encode_auth_token, decode_auth_token
from routes.routes import routes


class Api:
    def __init__(self, send: uvicorn) -> None:
        self.send = send
        self.params = None

    async def create_token(self, params: str) -> None:
        user_id = params[0].get("user_id")
        if not user_id:
            body = [{"error": bad_request_msg}]
            await self.send_response(body, status=400)
        else:
            res, token = await encode_auth_token(user_id)
            if res:
                return await self.send_response({"api-token": token}, status=200)
            return await self.send_response(
                {"Error": token_gen_failed, "msg": str(token)}, status=501
            )

    async def check_auth_token(self, token: str) -> bool:
        valid_token, user_id, msg = await decode_auth_token(token)
        if valid_token:
            return True
        else:
            body = [{"error": token_refused, "msg": msg}]
            await self.send_response(body, status=401)
        return False

    async def send_response(self, body: list, status: int = 200):
        await self.send(dict(http_response_start, **{"status": status}))
        body = json.dumps(body).encode("utf-8")
        await self.send(dict(http_response_body, **{"body": body}))

    async def parse_request(self, route: str, q: str) -> bool:
        if not q:
            body = [{"error": empty_msg}]
            return False, await self.send_response(body, status=400)

        dec = urllib.parse.unquote(q.decode())
        params = json.loads(dec)
        logging.info(params)

        if route == "/create_token/":
            await self.create_token(params)
            return True, params
        return False, params


async def app(scope, receive, send):

    assert scope["type"] == "http"
    q = scope["query_string"]
    h = scope["headers"]
    route = scope["path"]
    logging.info(route)

    api = Api(send)

    is_new_token, params = await api.parse_request(route, q)
    if not is_new_token:
        token = dict((x, y) for x, y in h).get(b"api-token").decode()
        logging.info(f"token: {token}  ::  params: {params}")
        is_authorised = await api.check_auth_token(token)
        if is_authorised:
            await routes[route](send, params, api.send_response)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=5000,
        log_level="info",
        reload=True,
        env_file="api.env",
    )
