#!/usr/bin/env python3
import argparse


class DurableState:
    def __init__(self):
        self.artifacts = set()
        self.completed = set()


def process_chunk(state: DurableState, chunk_id: str, scenario: str):
    artifact = f"results/{chunk_id}.json"

    print(f"start {chunk_id}")

    if scenario == "ai-429":
        print("AI -> 429 Retry-After: 2")
        print("action: defer, backoff+jitter, do not increase concurrency")
        return "WAITING_FOR_PROVIDER"

    if scenario == "r2-503":
        print("R2 PUT -> 503")
        print("action: retry failed object operation with bounded exponential backoff")
        return "RETRYING_STORAGE"

    # Imagine AI succeeded and artifact is durably written.
    state.artifacts.add(artifact)
    print("durable artifact written:", artifact)

    if scenario == "worker-crash":
        print("💥 worker crashes before DB completion / ACK")
        print("redelivery occurs")
        if artifact in state.artifacts:
            print("new worker detects existing deterministic artifact")
        state.completed.add(chunk_id)
        print("reconcile DB state and ACK")
        return "COMPLETED"

    if scenario == "db-down":
        print("PostgreSQL unavailable after durable output")
        print("action: keep/retry durable reconciliation; do not regenerate output blindly")
        return "WAITING_FOR_DB"

    state.completed.add(chunk_id)
    return "COMPLETED"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--scenario", choices=["worker-crash", "ai-429", "r2-503", "db-down", "healthy"], default="healthy")
    args = p.parse_args()
    state = DurableState()
    result = process_chunk(state, "job123/chunk037/v1", args.scenario)
    print("result:", result)
    print("artifacts:", sorted(state.artifacts))
    print("completed:", sorted(state.completed))


if __name__ == "__main__":
    main()
