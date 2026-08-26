#!/usr/bin/env python3
"""Redis Streams worker demonstrating at-least-once + idempotent durable effect."""

from __future__ import annotations

import argparse
import os
import sqlite3
import time
from pathlib import Path

import redis
from redis.exceptions import ResponseError

STREAM = "transcription:jobs"
GROUP = "transcription-workers"
DLQ = "transcription:dlq"
DB_PATH = Path(__file__).with_name("lab.db")


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS transcripts (
                job_id TEXT PRIMARY KEY,
                message_id TEXT NOT NULL,
                transcript TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_messages (
                message_id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                processed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def ensure_group(r: redis.Redis) -> None:
    try:
        r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
        print(f"created group {GROUP}")
    except ResponseError as exc:
        if "BUSYGROUP" not in str(exc):
            raise


def already_processed(message_id: str) -> bool:
    with sqlite3.connect(DB_PATH) as db:
        row = db.execute(
            "SELECT 1 FROM processed_messages WHERE message_id = ?",
            (message_id,),
        ).fetchone()
        return row is not None


def persist_success(message_id: str, job_id: str, transcript: str) -> None:
    """One local transaction makes the demo's durable effect duplicate-safe."""
    with sqlite3.connect(DB_PATH) as db:
        db.execute("BEGIN IMMEDIATE")
        db.execute(
            "INSERT OR IGNORE INTO transcripts(job_id, message_id, transcript) VALUES (?, ?, ?)",
            (job_id, message_id, transcript),
        )
        db.execute(
            "INSERT OR IGNORE INTO processed_messages(message_id, job_id) VALUES (?, ?)",
            (message_id, job_id),
        )
        db.commit()


def process_entry(r: redis.Redis, stream_id: str, fields: dict[str, str]) -> None:
    message_id = fields["message_id"]
    job_id = fields["job_id"]

    if already_processed(message_id):
        print(f"duplicate delivery: {message_id}; durable effect already exists → ACK")
        r.xack(STREAM, GROUP, stream_id)
        return

    if fields.get("kind") == "corrupt":
        print(f"permanent failure job={job_id} → DLQ")
        r.xadd(
            DLQ,
            {
                **fields,
                "original_stream_id": stream_id,
                "failure_class": "CORRUPT_MEDIA",
            },
        )
        r.xack(STREAM, GROUP, stream_id)
        return

    print(f"processing job={job_id} stream_id={stream_id}")
    time.sleep(1.0)  # stand-in for expensive work

    persist_success(
        message_id,
        job_id,
        transcript=f"mock transcript for {fields['media_key']}",
    )
    print(f"durable commit complete job={job_id}")

    # Demonstrates: DB effect committed, ACK lost because worker crashed.
    # Redis will still consider the entry pending. Reclaim/redeliver it and the
    # idempotency check above makes the duplicate harmless.
    if os.getenv("CRASH_AFTER_COMMIT") == "1":
        print("simulating crash AFTER durable commit but BEFORE XACK")
        os._exit(17)

    r.xack(STREAM, GROUP, stream_id)
    print(f"ACK job={job_id}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--consumer", default=f"worker-{os.getpid()}")
    args = parser.parse_args()

    init_db()
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    ensure_group(r)

    print(f"consumer={args.consumer} waiting...")
    while True:
        rows = r.xreadgroup(
            GROUP,
            args.consumer,
            {STREAM: ">"},
            count=1,
            block=5000,
        )
        if not rows:
            continue

        for _stream, entries in rows:
            for stream_id, fields in entries:
                process_entry(r, stream_id, fields)


if __name__ == "__main__":
    main()
