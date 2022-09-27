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
