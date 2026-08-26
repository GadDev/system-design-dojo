#!/usr/bin/env python3
"""Publish a tiny transcription-job reference to a Redis Stream."""

from __future__ import annotations

import argparse
import uuid
from datetime import datetime, timezone

import redis

STREAM = "transcription:jobs"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id", default=f"job_{uuid.uuid4().hex[:8]}")
    parser.add_argument("--media-key", default="uploads/demo.mp4")
    parser.add_argument(
        "--kind",
        choices=["normal", "corrupt"],
        default="normal",
        help="corrupt demonstrates permanent failure + DLQ",
    )
    args = parser.parse_args()

    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    message_id = f"msg_{uuid.uuid4().hex}"
    stream_id = r.xadd(
        STREAM,
        {
            "message_id": message_id,
            "job_id": args.job_id,
            "media_key": args.media_key,
            "kind": args.kind,
            "schema_version": "1",
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    print(f"published stream_id={stream_id} message_id={message_id} job_id={args.job_id}")


if __name__ == "__main__":
    main()
