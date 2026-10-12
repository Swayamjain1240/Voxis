from collections import deque
from time import monotonic


class WindowRateLimiter:
    """Bounded per-process limiter. Peer address comes from ASGI, not user headers."""

    def __init__(self, limit: int, window_seconds: int = 60, max_clients: int = 1024, clock=monotonic):
        self.limit = limit
        self.window_seconds = window_seconds
        self.max_clients = max_clients
        self.clock = clock
        self.clients = {}

    def allow(self, client: str) -> bool:
        now = self.clock()
        cutoff = now - self.window_seconds
        if client not in self.clients:
            if len(self.clients) >= self.max_clients:
                self.clients = {key: hits for key, hits in self.clients.items() if hits[-1] > cutoff}
            if len(self.clients) >= self.max_clients:
                return False
            self.clients[client] = deque()
        hits = self.clients[client]
        while hits and hits[0] <= cutoff:
            hits.popleft()
        if len(hits) >= self.limit:
            return False
        hits.append(now)
        return True
