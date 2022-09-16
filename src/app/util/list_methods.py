class Routes:
    async def register_address(params, send_response) -> None:
        body = [{"sucess": "registered"}]
        await send_response(body, status=200)

    def test(self):
        pass

    def create_token(self):
        pass

    def other(self):
        pass


routes = (
    "/register_address/",
    "/create_token",
)

ignore = [
    "__class__",
    "__delattr__",
    "__dict__",
    "__dir__",
    "__doc__",
    "__eq__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__gt__",
    "__hash__",
    "__init__",
    "__init_subclass__",
    "__le__",
    "__lt__",
    "__module__",
    "__ne__",
    "__new__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__setattr__",
    "__sizeof__",
    "__str__",
    "__subclasshook__",
    "__weakref__",
]

stripped = [x.split("/")[1] for x in routes]
print(stripped)
r = Routes()
methods = [x for x in dir(r) if x not in ignore and x in stripped]
print(methods)
