# Day 5 — Race Conditions, Distributed Locks & Idempotency

## Goal

Recognize coordination races, use the database and idempotency first, and understand when distributed locks are necessary — including their failure modes.

## Timebox

- 20 min — race conditions
- 20 min — lock-free correctness patterns
- 20 min — distributed-lock semantics
- 20 min — transcription race table
- 10 min — retrieval quiz

---

# 1. What is a race condition?

A race condition occurs when correctness depends on the relative timing/interleaving of concurrent operations.

Example:

```text
Worker A reads chunk = PENDING
Worker B reads chunk = PENDING

A processes
B processes

Both write result
```

The bug is not “two workers exist.”

The bug is that the state transition did not define what should happen under concurrency.

---

# 2. Common races in the transcription pipeline

## Duplicate chunk execution

Two consumers process the same chunk because delivery is at least once.

## Duplicate merge

Two actors observe that the barrier is satisfied.

## Counter drift

The same completion event increments parent progress twice.

## Cancel vs complete

User cancels while a worker commits success.

## Retry vs original worker

Retry starts because the original looks dead; original eventually finishes too.

## Pipeline reprocess race

Pipeline v2 starts while old v1 messages are still in flight.

These are normal distributed-system scenarios.

---

# 3. Prefer invariants to locks

Before reaching for a distributed lock, try:

- unique constraints,
- compare-and-set updates,
- idempotency keys,
- transactions,
- deterministic object keys,
- monotonic state transitions,
- version numbers.

Example:

```sql
UNIQUE(job_id, chunk_index, pipeline_version)
```

prevents duplicate logical child creation regardless of how many coordinators race.

---

# 4. Compare-and-set

Claim work:

```sql
UPDATE chunks
SET status = 'running', worker_id = :worker
WHERE id = :id
  AND status = 'pending';
```

Exactly one competing transaction should observe a successful claim.

This is simpler than:

```text
acquire distributed lock
read row
modify row
release lock
```

when the database row itself is the coordination point.

---

# 5. Optimistic versioning

You can add:

```text
version = 7
```

and update:

```sql
UPDATE jobs
SET status = :new_status,
    version = version + 1
WHERE id = :id
  AND version = :expected_version;
```

If zero rows update, someone else changed the job.

This makes the race explicit.

---

# 6. What is a distributed lock?

A distributed lock attempts to let only one process act as owner of some logical resource at a time.

Examples:

```text
lock:job:123:merge
lock:tenant:42:billing-rollup
```

Useful when multiple processes must coordinate exclusive work that cannot be protected sufficiently by a single atomic data-store operation.

But locks add their own distributed-systems problems.

---

# 7. Lease-based locks

Many distributed locks are leases:

```text
acquire lock for 30 seconds
```

Why a lease?

If the owner dies, the lock eventually expires.

But now ask:

> What if work takes 45 seconds?

A worker can still be alive after losing ownership.

This creates the **stale owner** problem.

---

# 8. Fencing tokens

A robust pattern pairs lock acquisition with an increasing token:

```text
Worker A acquires token 41
Worker B later acquires token 42
```

Downstream resource rejects operations using older token `41` once it has seen `42`.

The lock says:

```text
who *should* be owner
```

The fencing token helps the resource reject stale owners.

This is especially important for long-running work.

---

# 9. Redis locks: understand the caveats

Redis documents a distributed-lock approach and explicitly discusses safety, liveness, lease expiry and fencing-token considerations.

The important lesson is not “Redlock good” or “Redlock bad.”

It is:

> A distributed lock is a protocol with assumptions. Know which correctness guarantee your workload requires.

If merge can be made safe with a DB compare-and-set and idempotent final output, that is usually easier to reason about than building your correctness on a lock lease.

---

# 10. PostgreSQL advisory locks

PostgreSQL provides advisory locks for application-defined resources.

They can be:

- session-level,
- transaction-level.

Transaction-level advisory locks are released automatically when the transaction ends.

They are useful when all contenders coordinate through the same PostgreSQL primary and a natural row lock is inconvenient.

But they are not a replacement for durable state transitions.

---

# 11. Idempotency is still required

A lock does not eliminate retries.

Example:

```text
merge obtains lock
writes final transcript
network fails
caller does not know whether write succeeded
```

You still need deterministic/idempotent output behavior.

Good pattern:

```text
final transcript key:
jobs/{job_id}/v3/final.json
```

Repeated writes replace/verify the same logical artifact rather than creating unbounded duplicates.

---

# 12. Race-condition mitigation table

Complete this yourself:

| Race | Invariant | Preferred mechanism | Lock required? |
|---|---|---|---|
| Duplicate child creation | one child/index/version | DB unique constraint | ? |
| Duplicate worker delivery | one logical chunk result | idempotent write + CAS | ? |
| Duplicate merge | one logical merge claim | guarded parent transition | ? |
| Cancel vs complete | terminal-state policy | version/CAS/state machine | ? |
| Global singleton maintenance task | one active owner | lease/advisory lock maybe | ? |

The point is to make **locks the last question**, not the first.

---

# Exercise — Last two chunks finish together

Initial state:

```text
expected = 90
completed = 88
status = PROCESSING
```

Worker A completes chunk 88.
Worker B completes chunk 89 almost simultaneously.

Design a transaction/sequence that guarantees:

- both chunk results are durable,
- parent count reaches 90 exactly once,
- exactly one logical merge is claimed,
- duplicate delivery of either completion does not change correctness.

Do it once **without** a distributed lock.

Then describe what a lock-based design would add and why you prefer or reject it.

---

# Break it 💥

1. Worker acquires a 30s lock, pauses for 45s due to GC, then resumes.
2. Redis is partitioned from one worker.
3. PostgreSQL transaction rolls back after an advisory lock was acquired at transaction scope.
4. Two workers write the same deterministic object key.
5. A retried v1 chunk arrives during pipeline v2.

---

# Retrieval quiz

1. Define a race condition.
2. Name five races in the transcription workflow.
3. Why prefer unique constraints/CAS over locks when possible?
4. What is a lease?
5. What is the stale-owner problem?
6. What is a fencing token?
7. Why does a lock not remove the need for idempotency?
8. Session vs transaction advisory lock?
9. Why version chunk identity?
10. Give one case where a distributed lock may genuinely be appropriate.

## Exit criterion

You can explain **what invariant you are protecting**, and choose the smallest coordination mechanism that enforces it.
