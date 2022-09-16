async def register_address(send, params, send_response) -> None:
    body = [{"sucess": "registered"}]
    await send_response(send, body, status=200)


routes = {
    "/register_address/": register_address,
}
