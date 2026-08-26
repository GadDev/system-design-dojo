# Week 6 Cheat Sheet — Distributed Processing

## Core pipeline

```text
Parent
  ↓
Fan-out
  ↓
Child jobs → workers
  ↓
Durable child results
  ↓
Barrier
  ↓
Fan-in / merge
  ↓
Final result
```

## Fan-out

Split one logical workload into independently schedulable work units.

## Fan-in

Coordinate child results and combine them after a barrier condition is met.

## Concurrency

Multiple operations in progress at overlapping times.

## Parallelism

Multiple operations executing simultaneously on separate capacity.

## Straggler

A child task whose latency is much higher than peers and delays the fan-in barrier.

## Chunk-size tradeoff

```text
smaller
→ better retries/load balancing
→ more queue/metadata/merge overhead

larger
→ less overhead/more context
→ larger retry domain/worse stragglers
```

## Deterministic child identity

```text
(job_id, chunk_index, pipeline_version)
```

## Useful invariant

```sql
UNIQUE(job_id, chunk_index, pipeline_version)
```

## Parent progress

```text
completed_chunks / expected_chunks
```

But update only on a real durable state transition.

## Fan-in barrier

Strict example:

```text
all expected children SUCCEEDED
AND outputs durable
AND job not cancelled
```

## Merge ordering

```text
ORDER BY start_ms, chunk_index
```

Never completion order.

## Duplicate merge guard

```sql
UPDATE jobs
SET status = 'merging'
WHERE id = :id
  AND status = 'processing'
  AND completed_chunks = expected_chunks;
```

Only one successful logical claim.

## Race-condition toolkit

Prefer:

```text
unique constraint
CAS / guarded update
transaction
idempotency key
deterministic output key
versioning
```

before:

```text
distributed lock
```

## Distributed lock questions

```text
What is the lease duration?
What if the owner pauses past the lease?
How is ownership renewed?
How are stale owners fenced?
What happens during partition?
```

## Fencing token

Monotonically increasing ownership token that allows a downstream resource to reject stale owners.

## Orchestration choices

```text
DB + Queue
Celery group/chord
Temporal-style durable workflow
Managed workflow service
```

Choose from workflow requirements.

## Why chunk retry beats whole-video retry

```text
smaller failure domain
less wasted work
faster recovery
lower retry cost
preserves progress
better parallel scheduling
```

But creates:

```text
more tasks
more coordination
more races
merge complexity
stragglers
```

## Metrics

```text
chunk p50/p95/p99
chunk retry rate
queue age
active chunks
straggler ratio
merge wait/duration
duplicate suppressions
retry amplification
parent completion time
```

## Seven questions for any parallel stage

```text
1. What is the unit of work?
2. How is it identified?
3. What bounds concurrency?
4. What if it runs twice?
5. What if it never finishes?
6. What is the barrier?
7. How is finalization safe?
```
