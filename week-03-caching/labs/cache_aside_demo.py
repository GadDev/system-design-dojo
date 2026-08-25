"""
Week 3 cache-aside demo.

Requirements:
    pip install redis

Run Redis locally first:
    docker run --name system-design-redis -p 6379:6379 -d redis:8

Then:
    python cache_aside_demo.py
"""

import json
import time
from dataclasses import dataclass, asdict

import redis


client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Pretend this dictionary is PostgreSQL.
DATABASE = {
    "42": {
        "id": "42",
        "displayName": "Ada",
        "bio": "Distributed systems enthusiast",
        "version": 1,
    }
}


CACHE_TTL_SECONDS = 15


def cache_key(user_id: str) -> str:
    return f"profile:v1:{user_id}"


def database_read(user_id: str):
    print("DB READ")
    time.sleep(0.05)  # Artificial origin cost.
    return DATABASE.get(user_id)


def get_profile(user_id: str):
    key = cache_key(user_id)

    cached = client.get(key)
    if cached is not None:
        print("CACHE HIT")
        return json.loads(cached)

    print("CACHE MISS")
    value = database_read(user_id)

    if value is None:
        # Short negative cache for demo purposes.
        client.set(key, json.dumps({"_missing": True}), ex=3)
        return None

    client.set(key, json.dumps(value), ex=CACHE_TTL_SECONDS)
    return value


def update_profile(user_id: str, display_name: str):
    # Source of truth first.
    profile = DATABASE[user_id]
    profile["displayName"] = display_name
    profile["version"] += 1

    print("DB WRITE")

    # Then invalidate derived copy.
    client.delete(cache_key(user_id))
    print("CACHE INVALIDATE")


if __name__ == "__main__":
    client.flushdb()

    print("\n1) First read")
    print(get_profile("42"))

    print("\n2) Second read")
    print(get_profile("42"))

    print("\n3) Update")
    update_profile("42", "Ada Lovelace")

    print("\n4) Read after invalidation")
    print(get_profile("42"))

    print("\n5) Read again")
    print(get_profile("42"))

    print("\n6) Missing record")
    print(get_profile("999"))

    print("\n7) Missing record again — negative cache caveat")
    value = client.get(cache_key("999"))
    if value:
        parsed = json.loads(value)
        if parsed.get("_missing"):
            print("NEGATIVE CACHE HIT")
