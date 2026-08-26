import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def load_events(path: Path, job_id: str):
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if event.get("job_id") == job_id:
            events.append(event)
    return sorted(events, key=lambda e: e["timestamp"])


def investigate(events):
    if not events:
        return ["No events found for job."]

    output = []
    output.append(f"events: {len(events)}")
    output.append(f"first: {events[0]['timestamp']} {events[0]['event']}")
    output.append(f"last:  {events[-1]['timestamp']} {events[-1]['event']}")

    by_chunk = defaultdict(list)
    for event in events:
        if "chunk_index" in event:
            by_chunk[event["chunk_index"]].append(event)

    output.append("\nchunk summary:")
    for chunk_index in sorted(by_chunk):
        chunk_events = by_chunk[chunk_index]
        names = [e["event"] for e in chunk_events]
        completed = "chunk.completed" in names
        last = chunk_events[-1]
        output.append(
            f"  chunk {chunk_index}: {'COMPLETED' if completed else 'NOT COMPLETE'}; "
            f"last={last['event']} attempt={last.get('attempt', '-') }"
        )

    errors = Counter(
        e.get("error_class")
        for e in events
        if e.get("error_class")
    )
    if errors:
        output.append("\nnormalized errors:")
        for name, count in errors.most_common():
            output.append(f"  {name}: {count}")

    unfinished = []
    for chunk_index, chunk_events in by_chunk.items():
        if not any(e["event"] == "chunk.completed" for e in chunk_events):
            unfinished.append(chunk_index)

    output.append("\nworking hypothesis:")
    if unfinished:
        output.append(f"  fan-in is blocked by unfinished chunk(s): {unfinished}")
    if errors.get("rate_limited"):
        output.append("  evidence shows AI/provider rate limiting on the blocked chunk")
    if any(e["event"] == "chunk.retry_deferred" for e in events):
        output.append("  retries are currently deferred; inspect provider/circuit-breaker metrics")

    output.append("\nnext evidence to fetch:")
    output.append("  1. authoritative job/chunk rows in PostgreSQL")
    output.append("  2. fleet-wide AI 429 rate around this window")
    output.append("  3. trace(s) for the unfinished chunk")
    output.append("  4. queue age/depth and worker utilization")
    return output


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: python stuck_job_investigator.py EVENTS.jsonl JOB_ID")
    events = load_events(Path(sys.argv[1]), sys.argv[2])
    print("\n".join(investigate(events)))


if __name__ == "__main__":
    main()
