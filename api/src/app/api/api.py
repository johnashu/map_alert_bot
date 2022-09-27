import urllib.parse, json
import logging
from includes.messages import Messages
from auth.tokens import Token
from routes.routes import Routes


class Api(Routes, Messages, Token):
    def __init__(self, scope: dict, receive: dict, send: dict, *a, **kw) -> None:
        self.query = scope.get("query_string")
        self.headers = scope.get("headers")
        self.route = scope.get("path").split("/")[1]

        self.scope = scope
        self.send = send
        self.receive = receive

        self.params = None

    async def handle_scope(
        self,
    ) -> None:
        is_new_token = await self.parse_request()
        if not is_new_token:
            self.token = dict((x, y) for x, y in self.headers).get(b"api-token")
            if not self.token:
                body = [{"error": self.no_token_found}]
                return await self.send_response(body, status=400)
            else:
                self.token.decode()
                logging.info(f"token: {self.token}  ::  params: {self.params}")
                is_authorised = await self.check_auth_token()
                if is_authorised:
                    await self.__getattribute__(self.route)()

    async def send_response(self, body: list, status: int = 200):
        start = dict(self.http_response_start, **{"status": status})
        await self.send(start)
        body = json.dumps(body).encode("utf-8")
        response = dict(self.http_response_body, **{"body": body})
        await self.send(response)

    async def parse_request(self) -> bool:
        if not self.query:
            body = [{"error": self.empty_msg}]
            return False, await self.send_response(body, status=400)

        dec = urllib.parse.unquote(self.query.decode())
        self.params = json.loads(dec)

        if self.route == "new_token":
            await self.new_token()
            return True
        return False
