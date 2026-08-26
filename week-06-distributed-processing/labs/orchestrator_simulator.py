#!/usr/bin/env python3
"""Educational parent/child orchestrator simulator.

Demonstrates durable child identity, bounded concurrent processing, retry of a single
child, and an atomic PROCESSING -> MERGING claim.
"""
import asyncio
import random
import sqlite3
import tempfile
from pathlib import Path

SCHEMA = """
CREATE TABLE jobs (
  id TEXT PRIMARY KEY,
  status TEXT NOT NULL,
  expected_chunks INTEGER NOT NULL,
  completed_chunks INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE chunks (
  job_id TEXT NOT NULL,
  chunk_index INTEGER NOT NULL,
  status TEXT NOT NULL,
  attempts INTEGER NOT NULL DEFAULT 0,
  output TEXT,
  PRIMARY KEY(job_id, chunk_index)
);
"""

def connect(path):
    return sqlite3.connect(path, timeout=5)

def plan(path, n=12):
    con = connect(path)
    con.execute("INSERT INTO jobs VALUES ('job-1', 'processing', ?, 0)", (n,))
    con.executemany(
        "INSERT INTO chunks(job_id, chunk_index, status) VALUES ('job-1', ?, 'pending')",
        [(i,) for i in range(n)],
    )
    con.commit(); con.close()

async def run_chunk(path, index, sem):
    async with sem:
        await asyncio.sleep(random.uniform(0.02, 0.08))
        # Force one first-attempt failure to make retry visible.
        con = connect(path)
        attempts = con.execute(
            "SELECT attempts FROM chunks WHERE job_id='job-1' AND chunk_index=?", (index,)
        ).fetchone()[0]
        con.close()
        if index == 5 and attempts == 0:
            raise RuntimeError("synthetic transient failure")

        con = connect(path)
        con.execute("BEGIN IMMEDIATE")
        row = con.execute(
            "SELECT status FROM chunks WHERE job_id='job-1' AND chunk_index=?", (index,)
        ).fetchone()
        if row[0] != "succeeded":
            con.execute(
                "UPDATE chunks SET status='succeeded', attempts=attempts+1, output=? WHERE job_id='job-1' AND chunk_index=?",
                (f"text-{index}", index),
            )
            con.execute("UPDATE jobs SET completed_chunks=completed_chunks+1 WHERE id='job-1'")
        con.commit(); con.close()

async def process_all(path, concurrency=4):
    sem = asyncio.Semaphore(concurrency)
    pending = list(range(12))
    while pending:
        tasks = [run_chunk(path, i, sem) for i in pending]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        retry = []
        for idx, result in zip(pending, results):
            if isinstance(result, Exception):
                con = connect(path)
                con.execute("UPDATE chunks SET attempts=attempts+1, status='retryable' WHERE job_id='job-1' AND chunk_index=?", (idx,))
                con.commit(); con.close()
                print("retrying chunk", idx)
                retry.append(idx)
        pending = retry


def claim_merge(path):
    con = connect(path)
    con.execute("BEGIN IMMEDIATE")
    row = con.execute("SELECT expected_chunks, completed_chunks FROM jobs WHERE id='job-1'").fetchone()
    if row[0] != row[1]:
        con.rollback(); con.close(); return False
    cur = con.execute(
        "UPDATE jobs SET status='merging' WHERE id='job-1' AND status='processing' AND completed_chunks=expected_chunks"
    )
    won = cur.rowcount == 1
    con.commit(); con.close()
    return won


def merge(path):
    con = connect(path)
    rows = con.execute(
        "SELECT chunk_index, output FROM chunks WHERE job_id='job-1' ORDER BY chunk_index"
    ).fetchall()
    text = " ".join(r[1] for r in rows)
    con.execute("UPDATE jobs SET status='completed' WHERE id='job-1' AND status='merging'")
    con.commit(); con.close()
    return text

async def main():
    with tempfile.TemporaryDirectory() as d:
        path = str(Path(d) / "workflow.db")
        con = connect(path); con.executescript(SCHEMA); con.close()
        plan(path)
        await process_all(path)
        print("merge claim A:", claim_merge(path))
        print("merge claim B:", claim_merge(path))
        print("final:", merge(path))

if __name__ == "__main__":
    asyncio.run(main())
