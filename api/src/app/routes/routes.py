import imp


class Routes:
    async def register_address(self) -> None:
        body = [{"success": "registered"}]
        await self.send_response(body, status=200)

    async def new_token(self) -> None:
        user_id = self.params[0].get("user_id")
        if not user_id:
            body = [{"error": self.bad_request_msg}]
            await self.send_response(body, status=400)
        else:
            res, token = await self.encode_auth_token(user_id)
            if res:
                return await self.send_response({"api-token": token}, status=200)
            return await self.send_response(
                {"Error": self.token_gen_failed, "msg": str(token)}, status=501
            )

    async def send_messageto_tg_bot(
        self, context: dict = {}, method_name: str = "sendMessage"
    ) -> None:
        import requests
        from includes.config import TG_API_KEY

        tg_url = f"https://api.telegram.org/bot{TG_API_KEY}/{method_name}"

        context = dict(
            chat_id=self.params[0].get("chat_id"), text=self.params[0].get("text")
        )
        try:
            res = requests.post(tg_url, params=context)
            j = res.json()
            body = [
                {
                    **{"success": "Message sent", "result": j, "request": tg_url},
                    **context,
                }
            ]
            await self.send_response(body, status=200)
        except requests.exceptions.ConnectionError as e:
            pass
