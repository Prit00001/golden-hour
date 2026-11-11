"""Abuse limits. The app is public and has no login, and every call spends paid Gnani credit, so the
server caps how much any one visitor, and all visitors together, can use.

ponytail: counters live in this process's memory (one uvicorn worker). Move them to Redis if the app
ever runs more than one worker or instance.
"""
import time
from collections import Counter, defaultdict, deque
from urllib.parse import urlsplit

MAX_CALLS = 20          # live calls at once, whole server
MAX_CALLS_IP = 3        # live calls at once, one visitor
CALL_SECONDS = 600      # longest live call; a full call takes about 2 minutes
MAX_TEXT = 500          # typed line, characters
MAX_HISTORY = 4000      # conversation so far, characters (only the tail is kept)
MAX_CASE = 20_000       # case JSON from the browser, characters
MAX_AUDIO = 2_000_000   # tap-to-record clip, bytes (25 s of 16 kHz WAV is 0.8 MB)
MAX_FRAME = 8192        # one live mic frame, bytes (the page sends 1,024)
MAX_WS_TEXT = 2 * MAX_CASE


class Window:
    """At most `n` events per key in the last `seconds`."""

    def __init__(self, n: int, seconds: float):
        self.n, self.seconds, self.hits = n, seconds, defaultdict(deque)

    def allow(self, key, now=None) -> bool:
        now = time.monotonic() if now is None else now
        if len(self.hits) > 5000:  # forget visitors with nothing recent, so the table can't grow without end
            self.hits = defaultdict(deque, {k: q for k, q in self.hits.items() if q and now - q[-1] < self.seconds})
        q = self.hits[key]
        while q and now - q[0] >= self.seconds:
            q.popleft()
        if len(q) >= self.n:
            return False
        q.append(now)
        return True


calls_ip = Window(30, 3600)      # live calls per visitor per hour
calls_all = Window(400, 86400)   # live calls per day, everyone: the credit backstop if IPs are spoofed
turns_ip = Window(60, 600)       # fallback /turn requests per visitor per 10 minutes
turns_all = Window(3000, 86400)
active = Counter()               # live calls open now, per visitor


def client_ip(conn) -> str:
    """Best effort. Behind Render the real address is in cf-connecting-ip; uvicorn --proxy-headers covers the rest."""
    return conn.headers.get("cf-connecting-ip") or (conn.client.host if conn.client else "?")


def same_origin(headers) -> bool:
    """Stops other websites from using this server through a visitor's browser. Scripts send no Origin
    and are let through here; the limits above are what bound them."""
    origin = headers.get("origin")
    return not origin or urlsplit(origin).netloc in (headers.get("host"), headers.get("x-forwarded-host"))


def admit_call(ip: str) -> bool:
    if sum(active.values()) >= MAX_CALLS or active[ip] >= MAX_CALLS_IP:
        return False
    if not (calls_ip.allow(ip) and calls_all.allow("")):
        return False
    active[ip] += 1
    return True


def release_call(ip: str):
    active[ip] -= 1
    if active[ip] <= 0:
        del active[ip]


def admit_turn(ip: str) -> bool:
    return turns_ip.allow(ip) and turns_all.allow("")
