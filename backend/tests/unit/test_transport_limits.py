import asyncio

from app.core.config import Settings
from app.core.limits import WindowRateLimiter
from app.core.transport import JSON_LIMIT, MAX_INFLIGHT, TransportMiddleware


def scope(headers=()):
    return {"type": "http", "asgi": {"version": "3.0"}, "method": "POST", "path": "/",
            "scheme": "http", "query_string": b"", "client": ("127.0.0.1", 1),
            "headers": [(b"host", b"localhost"), *headers]}


async def never_called(*_args):
    raise AssertionError("Rejected input must not reach the handler")


def test_chunked_body_is_limited_without_content_length():
    async def run():
        received, sent = 0, []

        async def receive():
            nonlocal received
            received += 1
            return {"type": "http.request", "body": b"x" * (JSON_LIMIT // 2 + 1), "more_body": True}

        async def send(message):
            sent.append(message)

        await TransportMiddleware(never_called, Settings())(scope(), receive, send)
        assert received == 2
        assert sent[0]["status"] == 413

    asyncio.run(run())


def test_slow_body_times_out_and_releases_capacity():
    async def run():
        sent = []

        async def receive():
            await asyncio.Event().wait()

        async def send(message):
            sent.append(message)

        middleware = TransportMiddleware(never_called, Settings(request_timeout_seconds=1))
        await middleware(scope(), receive, send)
        assert sent[0]["status"] == 408
        assert middleware.inflight == 0

    asyncio.run(run())


def test_concurrent_requests_are_bounded_and_capacity_recovers():
    async def run():
        release, entered = asyncio.Event(), asyncio.Queue()

        async def handler(_scope, _receive, send):
            await entered.put(True)
            await release.wait()
            await send({"type": "http.response.start", "status": 204, "headers": []})
            await send({"type": "http.response.body", "body": b""})

        middleware = TransportMiddleware(handler, Settings())

        async def request():
            sent = []

            async def receive():
                return {"type": "http.request", "body": b""}

            async def send(message):
                sent.append(message)

            await middleware(scope(), receive, send)
            return sent[0]["status"]

        active = [asyncio.create_task(request()) for _ in range(MAX_INFLIGHT)]
        for _ in active:
            await asyncio.wait_for(entered.get(), 2)
        assert await request() == 503
        release.set()
        assert await asyncio.gather(*active) == [204] * MAX_INFLIGHT
        assert await request() == 204

    asyncio.run(run())


def test_rate_limit_expiry_is_bounded_across_client_churn():
    now = [100]
    limiter = WindowRateLimiter(2, max_clients=2, clock=lambda: now[0])
    assert limiter.allow("a") and limiter.allow("a")
    assert not limiter.allow("a")
    assert limiter.allow("b")
    assert not limiter.allow("c")
    now[0] += 60
    assert limiter.allow("c") and limiter.allow("a")
