from uuid import uuid4


class RequestContextMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        request_id = uuid4().hex
        scope.setdefault("state", {})["request_id"] = request_id

        async def with_request_id(message):
            if message["type"] == "http.response.start":
                message = {**message, "headers": [
                    *message.get("headers", []), (b"x-request-id", request_id.encode("ascii")),
                ]}
            await send(message)

        await self.app(scope, receive, with_request_id)
