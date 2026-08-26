from dataclasses import dataclass


@dataclass
class ChunkRow:
    status: str = "RUNNING"
    artifact_key: str | None = None
    accepted_count: int = 0


OBJECT_STORE: dict[str, dict] = {}
row = ChunkRow()
key = "results/job-123/v3/chunk-42.json"


def expensive_transcription():
    print("AI: expensive transcription executed")
    return {"text": "hello distributed world", "pipeline_version": 3, "checksum": "abc123"}


def write_artifact(result):
    OBJECT_STORE[key] = result
    print("R2: artifact written", key)


def finalize_db(simulate_failure=False):
    global row
    if simulate_failure:
        raise ConnectionError("PostgreSQL unavailable after artifact write")
    if row.status == "SUCCEEDED":
        print("DB: already SUCCEEDED — idempotent duplicate")
        return
    row.status = "SUCCEEDED"
    row.artifact_key = key
    row.accepted_count = 1
    print("DB: reconciled to SUCCEEDED")


def attempt(number, fail_db=False):
    print(f"\n--- attempt {number} ---")
    if row.status == "SUCCEEDED":
        print("worker: durable state already accepted; ACK")
        return

    artifact = OBJECT_STORE.get(key)
    if artifact and artifact.get("pipeline_version") == 3 and artifact.get("checksum") == "abc123":
        print("worker: valid deterministic artifact already exists; skip AI recomputation")
    else:
        artifact = expensive_transcription()
        write_artifact(artifact)

    finalize_db(simulate_failure=fail_db)
    print("worker: ACK")


try:
    attempt(1, fail_db=True)
except ConnectionError as exc:
    print("worker crashes/does not ACK:", exc)

attempt(2, fail_db=False)
print("\nfinal row:", row)
print("artifact count:", len(OBJECT_STORE))
