class Routes:
    async def register_address(params, send_response) -> None:
        body = [{"sucess": "registered"}]
        await send_response(body, status=200)


routes = (
    "/register_address/",
    "/create_token",
)
