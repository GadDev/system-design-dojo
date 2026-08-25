"""Simple Redis fixed-window rate-limit demo for Week 4.

Requires:
    pip install redis
    docker run --rm -p 6379:6379 redis:8

This is intentionally educational, not a production rate-limit library.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import redis


@dataclass
class Decision:
    allowed: bool
    count: int
    retry_after_seconds: int


def allow_request(
    client: redis.Redis,
    identity: str,
    *,
    limit: int = 5,
    window_seconds: int = 10,
) -> Decision:
    window = int(time.time()) // window_seconds
    key = f"ratelimit:{identity}:{window}"

    # Pipeline/transaction keeps increment and expiry together for this demo.
    pipe = client.pipeline(transaction=True)
    pipe.incr(key)
    pipe.expire(key, window_seconds + 1)
    count, _ = pipe.execute()

    ttl = max(client.ttl(key), 0)
    return Decision(
        allowed=count <= limit,
        count=int(count),
        retry_after_seconds=ttl if count > limit else 0,
    )


def main() -> None:
    client = redis.Redis(host="localhost", port=6379, decode_responses=True)

    identity = "user-42"
    for i in range(1, 9):
        decision = allow_request(client, identity)
        print(i, decision)
        time.sleep(0.25)


if __name__ == "__main__":
    main()
