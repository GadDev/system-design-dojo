#!/usr/bin/env python3
"""Claim stale pending Redis Stream messages after a worker disappears."""

from __future__ import annotations

import argparse

import redis

STREAM = "transcription:jobs"
GROUP = "transcription-workers"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--consumer", default="recovery-worker")
    parser.add_argument("--idle-ms", type=int, default=1000)
    args = parser.parse_args()

    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    result = r.xautoclaim(
        STREAM,
        GROUP,
        args.consumer,
        min_idle_time=args.idle_ms,
        start_id="0-0",
        count=10,
    )

    next_id, entries, *_ = result
    print(f"next_cursor={next_id} claimed={len(entries)}")
    for stream_id, fields in entries:
        print(stream_id, fields)
        # We intentionally do not process/ACK here. The normal worker lesson is
        # to understand ownership recovery; inspect XPENDING afterward.


if __name__ == "__main__":
    main()
