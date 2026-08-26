# Day 3 — Parent/Child Jobs, Orchestration & Bounded Concurrency

## Goal

Model the workflow explicitly so that it can survive worker crashes, duplicate events, restarts and large bursts without losing track of the parent job.

## Timebox

- 20 min — parent/child state model
- 20 min — orchestration vs choreography
- 20 min — bounded concurrency
- 20 min — state-machine exercise
- 10 min — retrieval quiz

---

# 1. Parent and child jobs

One video is one **logical parent job**.

The parallel tasks are **child jobs**.

```text
Parent Job: job_123
  ├── Chunk 0
  ├── Chunk 1
  ├── Chunk 2
  └── ...
```

The parent should not rely on one worker's memory to know what children exist.

Persist the plan.

---

# 2. Example schema

```sql
CREATE TABLE jobs (
    id uuid PRIMARY KEY,
    upload_id uuid NOT NULL,
    status text NOT NULL,
    expected_chunks integer NOT NULL DEFAULT 0,
    completed_chunks integer NOT NULL DEFAULT 0,
    failed_chunks integer NOT NULL DEFAULT 0,
    pipeline_version integer NOT NULL,
    merge_started_at timestamptz,
    completed_at timestamptz
);

CREATE TABLE chunks (
    id uuid PRIMARY KEY,
    job_id uuid NOT NULL REFERENCES jobs(id),
    chunk_index integer NOT NULL,
    start_ms bigint NOT NULL,
    end_ms bigint NOT NULL,
    status text NOT NULL,
    attempt_count integer NOT NULL DEFAULT 0,
    output_uri text,
    pipeline_version integer NOT NULL,
    UNIQUE(job_id, chunk_index, pipeline_version)
);
```

This does not solve the entire workflow.

It gives you a durable coordination surface.

---

# 3. State machines

Define allowed transitions.

## Parent

```text
CREATED
  ↓
PREPARING
  ↓
PROCESSING
  ↓
MERGING
  ↓
COMPLETED
```

Side paths:

```text
PROCESSING → FAILED
PROCESSING → CANCELLING → CANCELLED
MERGING    → FAILED
```

## Child

```text
PENDING → RUNNING → SUCCEEDED
             │
             ├→ RETRYABLE
             └→ FAILED
```

Transitions should be guarded, not arbitrary string updates.

---

# 4. Compare-and-set transitions

Instead of:

```sql
UPDATE chunks
SET status = 'running'
WHERE id = :id;
```

prefer a guarded transition:

```sql
UPDATE chunks
SET status = 'running'
WHERE id = :id
  AND status IN ('pending', 'retryable');
```

Then check affected row count.

This is a simple compare-and-set style pattern.

It often removes the need for a distributed lock.

---

# 5. Orchestration vs choreography

## Orchestration

A coordinator knows workflow state and decides the next step.

```text
Orchestrator
   ├→ split
   ├→ enqueue chunks
   ├→ wait
   └→ merge
```

Advantages:

- explicit workflow state,
- easier to inspect,
- centralized policy.

Tradeoffs:

- orchestrator correctness matters,
- can become a bottleneck if badly designed,
- workflow engine may add infrastructure.

## Choreography

Components react to events without one central workflow owner.

```text
upload.completed
      ↓
chunker emits chunk.created
      ↓
workers emit chunk.completed
      ↓
aggregator reacts
```

Advantages:

- loose coupling,
- easy to add subscribers.

Tradeoffs:

- workflow becomes implicit,
- debugging long chains is harder,
- race conditions can be less obvious.

For a long-running multi-stage transcription workflow, explicit orchestration is often easier to reason about.

---

# 6. Bounded concurrency

The orchestrator should not create unbounded load.

Useful controls:

```text
global worker concurrency
per-provider concurrency
per-tenant concurrency
per-parent-job concurrency
GPU pool capacity
```

Example:

```text
global           500
provider          100
enterprise tenant  30
free tenant         5
per video           10
```

The effective concurrency is the tightest relevant bound.

---

# 7. Fairness

Without fairness:

```text
One customer uploads 1,000 videos
          ↓
occupies every worker
          ↓
other customers wait
```

Possible strategies:

- per-tenant concurrency limits,
- tenant-specific queues,
- weighted fair scheduling,
- priority classes,
- round-robin dequeue across tenants.

Priority is useful, but starvation is a real risk.

---

# 8. Progress is derived state

For a simple model:

```text
progress = completed_chunks / expected_chunks
```

But what does “completed” mean?

Prefer:

```text
chunk output is durably stored
AND
chunk state is SUCCEEDED
```

Do not count “worker started” as durable progress.

You may reserve progress ranges by stage:

```text
upload      0–20%
prepare    20–30%
transcribe 30–90%
merge      90–100%
```

This creates a smoother UX than a single chunk counter.

---

# 9. Cancellation

Cancellation is not just:

```sql
status = 'cancelled'
```

You need semantics.

Questions:

- Do running chunks stop immediately or finish?
- Are queued chunks revoked/skipped?
- What happens to partial outputs?
- Can cancellation race with completion?
- Who wins if the merge has already begun?

A safe model can use a desired state:

```text
job.desired_state = CANCELLED
```

Workers check before expensive work and before committing final state.

The parent finalizer also checks it.

---

# 10. Orchestrator restart

A robust workflow cannot depend on volatile in-memory counters.

After restart, the orchestrator should reconstruct:

```text
expected chunks
completed chunks
failed chunks
merge state
```

from durable state or replayable workflow history.

That is one of the big reasons workflow engines exist.

---

# Exercise — Build the workflow state machine

Design states for:

```text
Upload complete
→ extract audio
→ plan chunks
→ enqueue chunks
→ transcribe
→ merge
→ finalize
```

For every transition define:

```text
trigger
precondition
durable effect
retry behavior
failure state
```

Then answer:

> If the orchestrator crashes after publishing 40 of 90 chunk messages, how does it safely continue?

A strong answer requires deterministic child identity and idempotent publication/creation.

---

# Break it 💥

1. The orchestrator publishes chunk 42 twice.
2. The orchestrator crashes after creating DB child rows but before publishing messages.
3. One enterprise customer's jobs occupy every worker.
4. A user cancels while the final two chunks complete.
5. The orchestrator restarts and its in-memory count says zero completed chunks.

---

# Retrieval quiz

1. Why persist the fan-out plan?
2. Parent job vs child job?
3. Why use guarded state transitions?
4. Orchestration vs choreography?
5. Name four useful concurrency limits.
6. What is starvation?
7. What should “chunk completed” mean?
8. Why is cancellation a distributed workflow concern?
9. What must an orchestrator reconstruct after restart?
10. Which correctness mechanisms can eliminate some lock requirements?

## Exit criterion

You can draw the workflow as a durable state machine and explain how it resumes after a crash.
