import uvicorn
import urllib.parse, json
import logging
from includes.messages import *
from users.tokens import encode_auth_token, decode_auth_token
from routes.routes import routes


class Api:
    def __init__(self, scope: dict, receive: dict, send: dict, *a, **kw) -> None:
        self.query = scope.get("query_string")
        self.headers = scope.get("headers")
        self.route = scope.get("path").split("/")[1]

        self.scope = scope
        self.send = send
        self.receive = receive

        self.params = None

        logging.info(self.route)

    async def handle_scope(
        self,
    ) -> None:
        is_new_token = await self.parse_request()
        if not is_new_token:
            self.token = (
                dict((x, y) for x, y in self.headers).get(b"api-token").decode()
            )
            logging.info(f"token: {self.token}  ::  params: {self.params}")
            is_authorised = await self.check_auth_token()
            if is_authorised:
                await self.__getattribute__(self.route)()

    async def register_address(self) -> None:
        body = [{"success": "registered"}]
        await self.send_response(body, status=200)

    async def create_token(self) -> None:
        user_id = self.params[0].get("user_id")
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

    async def check_auth_token(self) -> bool:
        valid_token, user_id, msg = await decode_auth_token(self.token)
        if valid_token:
            return True
        else:
            body = [{"error": token_refused, "msg": msg}]
            await self.send_response(body, status=401)
        return False

    async def send_response(self, body: list, status: int = 200):
        start = dict(http_response_start, **{"status": status})
        await self.send(start)
        body = json.dumps(body).encode("utf-8")
        response = dict(http_response_body, **{"body": body})
        await self.send(response)

    async def parse_request(self) -> bool:
        if not self.query:
            body = [{"error": empty_msg}]
            return False, await self.send_response(body, status=400)

        dec = urllib.parse.unquote(self.query.decode())
        self.params = json.loads(dec)
        logging.info(self.params)

        if self.route == "/create_token/":
            await self.create_token()
            return True
        return False


async def app(scope, receive, send):

    assert scope["type"] == "http"
    api = Api(scope, receive, send)
    await api.handle_scope()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=5000,
        log_level="info",
        reload=True,
        env_file="api.env",
    )
