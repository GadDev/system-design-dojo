"""Small saga-orchestration simulation with business compensation."""

from dataclasses import dataclass, field


@dataclass
class Saga:
    saga_id: str
    job_id: str
    state: str = "REQUESTED"
    completed_steps: set[str] = field(default_factory=set)
    compensations: list[str] = field(default_factory=list)


def once(saga: Saga, step: str, fn) -> None:
    if step in saga.completed_steps:
        print(f"skip duplicate step: {step}")
        return
    fn()
    saga.completed_steps.add(step)


def stop_processing() -> None:
    print("processing stopped")


def release_quota() -> None:
    print("quota released")


def reserve_quota_again() -> None:
    print("COMPENSATION: quota reserved again")


def finalize_cancel() -> None:
    raise RuntimeError("simulated Jobs DB outage")


def run(saga: Saga) -> None:
    try:
        saga.state = "STOPPING_PROCESSING"
        once(saga, "stop_processing", stop_processing)

        saga.state = "RELEASING_QUOTA"
        once(saga, "release_quota", release_quota)

        saga.state = "FINALIZING"
        once(saga, "finalize_cancel", finalize_cancel)

        saga.state = "COMPLETED"
    except RuntimeError as exc:
        print("failure:", exc)
        saga.state = "COMPENSATING"
        if "release_quota" in saga.completed_steps:
            reserve_quota_again()
            saga.compensations.append("reserve_quota_again")
        saga.state = "FAILED_COMPENSATED"


def main() -> None:
    saga = Saga("saga-1", "job-123")
    run(saga)
    print("final saga:", saga)


if __name__ == "__main__":
    main()
