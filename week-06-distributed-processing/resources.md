# Week 6 — Sources & Reading Map

Use primary documentation and papers first. The goal is to understand the **mechanism**, then generalize it into an architecture pattern.

---

# Day 1 — Fan-out / Fan-in / Parallelism

## Google MapReduce paper

**Jeffrey Dean & Sanjay Ghemawat — “MapReduce: Simplified Data Processing on Large Clusters”**

https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/

Read for:

- map/reduce mental model,
- partitioning input,
- scheduling work across machines,
- handling worker failure,
- why frameworks hide distributed-execution plumbing.

Do **not** conclude that your transcription system should use Hadoop/MapReduce. We are borrowing the mental model.

---

# Day 2 — Partitioning / Media Segmentation

## FFmpeg Formats — segment muxer

https://ffmpeg.org/ffmpeg-formats.html#segment_002c-stream_005fsegment_002c-ssegment

Read for:

- segment muxer behavior,
- `segment_time`,
- segment lists,
- start/end metadata,
- keyframe caveats for video segmentation.

For transcription, remember that you will usually extract/normalize audio first, which changes the segmentation problem.

---

# Day 3–4 — Workflow Fan-Out / Fan-In

## Celery Canvas

https://docs.celeryq.dev/en/main/userguide/canvas.html

Focus on:

- `group`,
- `chain`,
- `chord`,
- result collection.

A **group** is a concrete fan-out primitive. A **chord** is a group with a callback that runs after the group completes — a concrete fan-in primitive.

## AWS Step Functions — Map state

https://docs.aws.amazon.com/step-functions/latest/dg/state-map.html

Read for:

- bounded parallel iteration,
- parent/child workflow executions,
- explicit concurrency controls.

## AWS Step Functions — Distributed Map

https://docs.aws.amazon.com/step-functions/latest/dg/state-map-distributed.html

Read for:

- high-concurrency child workflows,
- `MaxConcurrency`,
- failure thresholds,
- separate execution histories.

Treat AWS as a concrete implementation of general orchestration ideas, not as the only architecture.

---

# Day 5 — Distributed Locks / Race Conditions

## Redis — Distributed Locks

https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/

Read carefully, including the consistency disclaimer.

Focus on:

- mutual exclusion,
- liveness,
- lease expiry,
- failure assumptions,
- fencing-token discussion.

Important course lesson:

> A distributed lock is not automatically a correctness proof.

## PostgreSQL — Explicit / Advisory Locking

https://www.postgresql.org/docs/current/explicit-locking.html

Read for:

- session-level advisory locks,
- transaction-level advisory locks,
- automatic release at transaction end,
- observing locks via `pg_locks`.

Then compare a lock with a guarded `UPDATE ... WHERE status = ...`.

---

# Day 6 — Durable Workflow Engines

## Temporal Documentation

https://docs.temporal.io/

Use it to understand the durable-execution mental model:

- workflow state survives process/infrastructure failure,
- coordination logic and side-effecting activities are separated,
- retries/timers/workflow history become first-class concepts.

Do not study Temporal as a prerequisite to Week 6. It is an example of what a mature orchestrator can provide when custom workflow state becomes painful.

---

# Books

## Designing Data-Intensive Applications, 2nd Edition

Use the sections/chapters related to:

- partitioning,
- distributed failure,
- dataflow / batch processing,
- stream/message processing,
- consistency and coordination.

Questions to ask while reading:

```text
What is the unit of failure?
What state is durable?
What happens after retry?
What coordination does this design require?
```

## Designing Distributed Systems — Brendan Burns

Useful patterns:

- replicated load-balanced services,
- work queues,
- scatter/gather,
- orchestration patterns.

“Scatter/gather” maps nicely to fan-out/fan-in thinking.

## Enterprise Integration Patterns — Hohpe & Woolf

Useful vocabulary:

- aggregator,
- idempotent receiver,
- competing consumers,
- correlation identifier,
- message sequence.

## Release It!, 2nd Edition

Use for:

- timeouts,
- overload,
- bulkheads,
- stability boundaries,
- failure amplification.

---

# Suggested daily reading

```text
Day 1 → Google MapReduce paper abstract + model/failure sections
Day 2 → FFmpeg segment muxer + DDIA partitioning intuition
Day 3 → Celery groups/chords + Step Functions Map overview
Day 4 → re-read chord/Map fan-in behavior; focus on stragglers/results
Day 5 → Redis lock document + PostgreSQL advisory locks
Day 6 → Temporal overview + Step Functions Distributed Map
Day 7 → no new reading; design first, then compare your choices
```

---

# Source-evaluation rule

For each source, write three lines:

```text
Mechanism:
Guarantee:
Still my responsibility:
```

Example:

```text
Mechanism: Celery chord waits for a group before callback.
Guarantee: Framework coordinates callback readiness according to its backend semantics.
Still my responsibility: idempotent chunk effects, deterministic merge, business invariants, capacity.
```

That final line is the distributed-systems muscle we are building.
