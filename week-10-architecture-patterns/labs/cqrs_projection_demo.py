"""CQRS projection demo: authoritative writes, lagging read model."""

from dataclasses import dataclass


@dataclass
class Job:
    job_id: str
    status: str
    version: int
    filename: str


WRITE_DB: dict[str, Job] = {}
READ_MODEL: dict[str, dict] = {}
EVENTS: list[dict] = []
PROCESSED: set[str] = set()


def emit(event_type: str, job: Job) -> dict:
    event = {
        "event_id": f"evt-{len(EVENTS) + 1}",
        "type": event_type,
        "job_id": job.job_id,
        "version": job.version,
        "status": job.status,
        "filename": job.filename,
    }
    EVENTS.append(event)
    return event


def create_job(job_id: str, filename: str) -> None:
    job = Job(job_id, "QUEUED", 1, filename)
    WRITE_DB[job_id] = job
    emit("JobCreated", job)


def cancel_job(job_id: str) -> None:
    job = WRITE_DB[job_id]
    job.status = "CANCELLED"
    job.version += 1
    emit("JobCancelled", job)


def apply_projection(event: dict) -> None:
    if event["event_id"] in PROCESSED:
        return
    current = READ_MODEL.get(event["job_id"])
    if current and event["version"] <= current["version"]:
        PROCESSED.add(event["event_id"])
        return
    READ_MODEL[event["job_id"]] = {
        "job_id": event["job_id"],
        "status": event["status"],
        "filename": event["filename"],
        "version": event["version"],
    }
    PROCESSED.add(event["event_id"])


def main() -> None:
    create_job("job-123", "meeting.mp4")
    apply_projection(EVENTS[0])
    print("after create:")
    print("write:", WRITE_DB["job-123"])
    print("read :", READ_MODEL["job-123"])

    cancel_job("job-123")
    print("\nafter cancel, before projection catches up:")
    print("write:", WRITE_DB["job-123"])
    print("read :", READ_MODEL["job-123"], "<- stale")

    apply_projection(EVENTS[1])
    apply_projection(EVENTS[1])  # duplicate delivery is harmless
    print("\nafter projection update:")
    print("read :", READ_MODEL["job-123"])


if __name__ == "__main__":
    main()
