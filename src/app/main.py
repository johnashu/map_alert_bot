import uvicorn
from api.api import Api


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
