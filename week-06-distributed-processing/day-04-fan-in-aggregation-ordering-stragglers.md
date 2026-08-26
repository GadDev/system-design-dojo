# Day 4 — Fan-In, Aggregation, Ordering, Stragglers & Progress

## Goal

Design the join point so the final transcript is created only from the correct durable child results, in deterministic order, without duplicate finalization.

## Timebox

- 20 min — barrier semantics
- 20 min — deterministic ordering
- 15 min — stragglers and failure thresholds
- 20 min — merge algorithm
- 10 min — retrieval quiz

---

# 1. The barrier

A **barrier** is the condition that must become true before fan-in can proceed.

Simple strict barrier:

```text
successful_chunks == expected_chunks
```

But real policies can differ.

Example tolerant workflow:

```text
successful >= 98%
AND
remaining chunks permanently failed
AND
product allows partial transcript
```

The barrier is a **business policy**, not just a counter.

---

# 2. Never trust only an in-memory counter

This is fragile:

```python
completed += 1
if completed == expected:
    merge()
```

Why?

- process restart loses the value,
- duplicate completion increments twice,
- multiple workers race,
- counter may advance before output is durable.

Use durable state and idempotent updates.

---

# 3. Counter approach with duplicate protection

One approach:

1. worker writes output,
2. worker transitions chunk from `RUNNING` to `SUCCEEDED`,
3. parent counter increments **only if** that transition changed a row,
4. merge is triggered through an exactly-once guard / idempotent finalizer.

Pseudo-transaction:

```sql
BEGIN;

UPDATE chunks
SET status = 'succeeded', output_uri = :uri
WHERE id = :chunk_id
  AND status != 'succeeded';

-- only if row_count = 1
UPDATE jobs
SET completed_chunks = completed_chunks + 1
WHERE id = :job_id;

COMMIT;
```

Even then, you need to think carefully about the merge trigger.

---

# 4. Query-derived barrier

Instead of maintaining a counter, the finalizer can query:

```sql
SELECT count(*)
FROM chunks
WHERE job_id = :job_id
  AND status = 'succeeded';
```

Pros:

- fewer counter-drift bugs.

Cons:

- repeated count queries can become expensive,
- index design matters,
- still need to prevent duplicate merge execution.

Often systems use both:

```text
counter for cheap progress
+ authoritative reconciliation query when finalizing
```

---

# 5. Ordering

Workers finish in arbitrary order:

```text
42, 7, 8, 89, 1, 3, ...
```

Transcript order is not completion order.

Merge by deterministic metadata:

```text
ORDER BY chunk_index
```

or better, by canonical start time if chunks are time-defined:

```text
ORDER BY start_ms, chunk_index
```

The queue should not be your ordering source of truth.

---

# 6. Deterministic merge

Given the same set of chunk results, repeated merge attempts should produce the same logical output.

That makes merge retryable.

A deterministic merge should specify:

- ordering field,
- overlap ownership/dedup rule,
- timestamp offset handling,
- missing-chunk policy,
- whitespace/punctuation normalization,
- pipeline version.

Example:

```text
Chunk 0 owns [0, 60s)
Chunk 1 owns [60s, 120s)
```

Even if each chunk has 2 seconds of overlap, canonical ownership prevents duplicate words from appearing twice.

---

# 7. The “last worker” race

A classic bug:

```text
Worker A finishes chunk 89
Worker B finishes chunk 90

A reads completed=89
B reads completed=89

A increments → 90 → starts merge
B increments → 90 → starts merge
```

Now two merges run.

Possible protection:

```sql
UPDATE jobs
SET status = 'merging', merge_started_at = now()
WHERE id = :job_id
  AND status = 'processing'
  AND completed_chunks = expected_chunks;
```

Only one caller should get `row_count = 1`.

This is often better than acquiring a distributed lock.

---

# 8. Stragglers

Fan-in completion time is often dominated by the slowest required child.

Measure:

```text
chunk p50
chunk p95
chunk p99
max chunk duration
```

A useful metric:

```text
straggler_ratio = max_chunk_duration / median_chunk_duration
```

If:

```text
median = 20s
max = 180s
```

then:

```text
straggler_ratio = 9×
```

That is worth investigating.

Possible causes:

- much longer chunk,
- noisy audio,
- provider throttling,
- worker CPU/GPU contention,
- network/storage slowness,
- retry delay.

---

# 9. Partial success

Should a transcript succeed with one missing chunk?

Possible policies:

## Strict

```text
all required chunks must succeed
```

Best for correctness.

## Partial

```text
merge available chunks
mark missing time ranges
```

Useful if a partial transcript still has product value.

## Fallback

```text
failed chunk
→ alternate provider / larger context retry
```

This is a product-level tradeoff.

---

# 10. Progress semantics

Chunk completion gives fine-grained progress, but avoid false precision.

If chunk costs vary significantly:

```text
completed_count / total_count
```

may not represent remaining wall-clock time.

Alternatives:

- weighted by media duration,
- weighted by historical processing cost,
- show stage + completed chunks instead of ETA.

For UX, honest progress is better than a fake “83 seconds remaining.”

---

# Exercise — Design the merge transaction

Write pseudocode for a safe finalizer that:

1. checks the parent is eligible,
2. verifies all required chunk rows are durable,
3. claims the merge stage exactly once,
4. reads chunk results in deterministic order,
5. merges them,
6. writes the final transcript,
7. marks the parent completed,
8. can be retried safely after a crash.

Then inject a crash after step 6.

How does retry avoid duplicate/incorrect final output?

---

# Break it 💥

1. Two finalizers start simultaneously.
2. Parent counter says 90/90 but one `output_uri` is null.
3. Chunk outputs arrive out of order.
4. Chunk 42 succeeds twice with two different outputs.
5. Merge writes object storage successfully but DB completion update fails.

---

# Retrieval quiz

1. What is a fan-in barrier?
2. Why is a barrier a business-policy decision?
3. Why can counters drift?
4. How can a guarded parent transition prevent duplicate finalization?
5. Why not use queue arrival order for transcript order?
6. What makes merge deterministic?
7. What is a straggler?
8. Why can count-based progress misrepresent ETA?
9. Strict vs partial success?
10. Why should the finalizer itself be idempotent?

## Exit criterion

You can explain exactly how the system knows it is safe to merge — and why only one logical final result is produced even if the finalizer runs more than once.
