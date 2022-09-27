import jwt
import datetime
from includes.config import SECRET_KEY


class Token:
    async def check_auth_token(self) -> bool:
        valid_token, user_id, msg = await self.decode_auth_token(self.token)
        if valid_token:
            return True
        else:
            body = [{"error": self.token_refused, "msg": msg}]
            await self.send_response(body, status=401)
        return False

    async def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        exp: expiration date of the token
        iat: the time the token is generated
        sub: the subject of the token (the user whom it identifies)
        :return: string
        """
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(days=999, seconds=5),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }
            return True, jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        except Exception as e:
            return False, e

    async def decode_auth_token(self, auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, SECRET_KEY, algorithms="HS256")
            print(payload)
            return True, payload["sub"], "success"
        except jwt.ExpiredSignatureError:
            return False, "Not Found", "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return False, "Not Found", "Invalid token. Please log in again."
