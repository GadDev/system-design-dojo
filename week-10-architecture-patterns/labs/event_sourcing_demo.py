"""Minimal event-sourced aggregate demo with optimistic stream version."""

from dataclasses import dataclass


EVENT_STORE: dict[str, list[dict]] = {}
SNAPSHOTS: dict[str, tuple[int, dict]] = {}


@dataclass
class JobState:
    status: str = "NONE"
    completed_chunks: int = 0


def evolve(state: JobState, event: dict) -> JobState:
    if event["type"] == "JobCreated":
        state.status = "QUEUED"
    elif event["type"] == "ProcessingStarted":
        state.status = "PROCESSING"
    elif event["type"] == "ChunkCompleted":
        state.completed_chunks += 1
    elif event["type"] == "JobCompleted":
        state.status = "COMPLETED"
    return state


def load(job_id: str) -> tuple[JobState, int]:
    stream = EVENT_STORE.get(job_id, [])
    snapshot_version, snapshot = SNAPSHOTS.get(
        job_id, (0, {"status": "NONE", "completed_chunks": 0})
    )
    state = JobState(**snapshot)
    for event in stream[snapshot_version:]:
        state = evolve(state, event)
    return state, len(stream)


def append(job_id: str, expected_version: int, event: dict) -> int:
    stream = EVENT_STORE.setdefault(job_id, [])
    if len(stream) != expected_version:
        raise RuntimeError(
            f"optimistic concurrency conflict: expected {expected_version}, actual {len(stream)}"
        )
    stream.append(event)
    return len(stream)


def snapshot(job_id: str) -> None:
    state, version = load(job_id)
    SNAPSHOTS[job_id] = (
        version,
        {"status": state.status, "completed_chunks": state.completed_chunks},
    )


def main() -> None:
    version = 0
    version = append("job-1", version, {"type": "JobCreated"})
    version = append("job-1", version, {"type": "ProcessingStarted"})
    version = append("job-1", version, {"type": "ChunkCompleted", "index": 0})
    snapshot("job-1")
    version = append("job-1", version, {"type": "ChunkCompleted", "index": 1})
    version = append("job-1", version, {"type": "JobCompleted"})

    state, current_version = load("job-1")
    print("state:", state)
    print("version:", current_version)
    print("events:", EVENT_STORE["job-1"])
    print("snapshot:", SNAPSHOTS["job-1"])

    try:
        append("job-1", 3, {"type": "JobCancelled"})
    except RuntimeError as exc:
        print("conflict:", exc)


if __name__ == "__main__":
    main()
