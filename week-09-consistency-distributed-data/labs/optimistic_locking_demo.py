import sqlite3
import threading
import tempfile
from pathlib import Path


def connect(path):
    conn = sqlite3.connect(path, timeout=5, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def actor(path, name, expected_version, new_status, barrier):
    conn = connect(path)
    row = conn.execute("SELECT status, version FROM jobs WHERE id='job-1'").fetchone()
    print(f"{name} read status={row[0]} version={row[1]}")
    barrier.wait()

    cur = conn.execute(
        """
        UPDATE jobs
        SET status=?, version=version+1
        WHERE id='job-1' AND version=? AND status='PROCESSING'
        """,
        (new_status, expected_version),
    )
    print(f"{name} update rows={cur.rowcount}")
    conn.close()


def main():
    path = Path(tempfile.gettempdir()) / "system_design_ninja_optimistic.db"
    if path.exists():
        path.unlink()

    conn = connect(path)
    conn.execute("CREATE TABLE jobs(id TEXT PRIMARY KEY, status TEXT, version INTEGER NOT NULL)")
    conn.execute("INSERT INTO jobs VALUES('job-1','PROCESSING',7)")
    conn.close()

    barrier = threading.Barrier(2)
    threads = [
        threading.Thread(target=actor, args=(path, "admin-cancel", 7, "CANCELLED", barrier)),
        threading.Thread(target=actor, args=(path, "worker-complete", 7, "COMPLETED", barrier)),
    ]
    for t in threads: t.start()
    for t in threads: t.join()

    conn = connect(path)
    final = conn.execute("SELECT status, version FROM jobs WHERE id='job-1'").fetchone()
    print(f"final status={final[0]} version={final[1]}")
    print("Exactly one actor should report rows=1; the other rows=0.")
    conn.close()


if __name__ == "__main__":
    main()
