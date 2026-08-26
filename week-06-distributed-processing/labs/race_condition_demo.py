#!/usr/bin/env python3
import sqlite3
import tempfile
import threading
from pathlib import Path

SCHEMA = """
CREATE TABLE chunks (
  job_id TEXT NOT NULL,
  chunk_index INTEGER NOT NULL,
  pipeline_version INTEGER NOT NULL,
  status TEXT NOT NULL,
  PRIMARY KEY(job_id, chunk_index, pipeline_version)
);
"""

def attempt_insert(db_path: str, worker: str):
    con = sqlite3.connect(db_path, timeout=5)
    try:
        con.execute(
            "INSERT INTO chunks(job_id, chunk_index, pipeline_version, status) VALUES (?, ?, ?, ?)",
            ("job-123", 42, 3, "pending"),
        )
        con.commit()
        print(worker, "created logical chunk")
    except sqlite3.IntegrityError:
        print(worker, "lost race safely: invariant already exists")
    finally:
        con.close()

def main():
    with tempfile.TemporaryDirectory() as d:
        db = str(Path(d) / "race.db")
        con = sqlite3.connect(db)
        con.executescript(SCHEMA)
        con.close()

        a = threading.Thread(target=attempt_insert, args=(db, "worker-A"))
        b = threading.Thread(target=attempt_insert, args=(db, "worker-B"))
        a.start(); b.start(); a.join(); b.join()

        con = sqlite3.connect(db)
        count = con.execute("SELECT count(*) FROM chunks").fetchone()[0]
        print("durable logical rows:", count)
        con.close()

if __name__ == "__main__":
    main()
