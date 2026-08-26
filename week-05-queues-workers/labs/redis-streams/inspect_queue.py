#!/usr/bin/env python3
"""Print a few useful Redis Streams queue-health signals."""

from __future__ import annotations

import redis

STREAM = "transcription:jobs"
GROUP = "transcription-workers"
DLQ = "transcription:dlq"

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

print("stream length:", r.xlen(STREAM))
print("dlq length:", r.xlen(DLQ) if r.exists(DLQ) else 0)

try:
    print("pending summary:", r.xpending(STREAM, GROUP))
    print("groups:", r.xinfo_groups(STREAM))
except redis.ResponseError as exc:
    print("group not created yet:", exc)
