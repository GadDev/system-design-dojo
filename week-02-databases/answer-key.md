# Week 2 — Selected Answer Key

Use this **after** attempting the exercises.

The goal is not to reproduce these answers exactly. The goal is to compare reasoning.

---

# Day 1

## Storage choices — one defensible starting point

```text
User metadata       → PostgreSQL
Original video      → object storage
Job state           → PostgreSQL
Chunk state/results → PostgreSQL initially
Final transcript    → PostgreSQL or hybrid; workload-dependent
Provider metadata   → PostgreSQL JSONB if small/operational
CSV export          → object storage
```

Why "initially" matters:

Chunk text may later become an object-storage or archival concern if row volume/size grows, but PostgreSQL is operationally simple while the scale is manageable.

---

# Day 2

## Suggested cardinality

```text
User    1 → N Uploads
Upload  1 → N Jobs
Job     1 → N Chunks
Job     1 → 0..1 canonical Transcript
```

Why multiple jobs per upload?

Reprocessing the same source with new model/settings should not necessarily destroy the history of the previous attempt.

## Duplicate chunks

Use:

```sql
UNIQUE(job_id, chunk_index)
```

That turns "workers won't duplicate it" into an enforceable invariant.

---

# Day 3

## Query A — job history

Candidate:

```sql
CREATE INDEX idx_jobs_user_created
ON jobs(user_id, created_at DESC);
```

## Query B — ordered chunks

Candidate:

```sql
CREATE INDEX idx_chunks_job_index
ON chunks(job_id, chunk_index);
```

Note: if `UNIQUE(job_id, chunk_index)` already exists, PostgreSQL already has an index that may satisfy this pattern. Avoid redundant duplicate indexes.

## Query C — active jobs

A partial index is plausible if completed jobs dominate:

```sql
CREATE INDEX idx_jobs_active_created
ON jobs(created_at)
WHERE status IN ('queued', 'processing');
```

---

# Day 4

## Safe chunk completion

Core ideas:

- transition the chunk only if it is not already done,
- increment parent progress only when a new transition occurred,
- keep both updates inside one transaction,
- retry the whole transaction on serialization/deadlock errors when appropriate,
- enforce unique chunk identity in the DB.

A single exact SQL implementation is intentionally not prescribed because ORM/queue design changes the mechanics.

---

# Day 5

Given:

```text
30 API × 10 = 300
80 workers × 5 = 400
```

Maximum potential DB connections:

```text
700
```

After doubling instance counts:

```text
1,400
```

This is why per-instance pool sizing must be considered together with autoscaling limits.

If pool wait grows while DB CPU is low, investigate:

- pool too small,
- long-held/idle transactions,
- lock waits,
- network issues,
- connection acquisition behavior.

If pool wait grows while DB CPU/I/O is saturated, creating more DB concurrency may worsen the bottleneck.

---

# Day 6

## Symptom mapping

### A — sequential scan over 80M rows

First investigate:

```text
query plan + index/selectivity/statistics
```

### B — DB CPU low, connection acquisition failing

Investigate:

```text
connection counts / pools / long-held connections
```

### C — stale-tolerant analytics dominate primary reads

Candidate:

```text
read replica
```

### D — time-bounded huge audit table + bulk retention deletion

Candidate:

```text
RANGE partitioning by time
```

### E — true optimized single-node write/storage ceiling

Now sharding becomes a legitimate conversation.

---

# Day 7 — Transcript storage decision

There is no universal answer.

A strong answer makes the tradeoff explicit.

## PostgreSQL-first is reasonable when

```text
transcripts are modest in size
search/query is frequent
simplicity matters
scale is still moderate
transactional metadata/content coupling is useful
```

## Object-storage-first is reasonable when

```text
transcripts/exports are large immutable artifacts
DB replication/backup volume is becoming material
most reads fetch the whole artifact
SQL search is not required
```

## Hybrid is often strong when

```text
PostgreSQL stores searchable structured segments/metadata
object storage stores the canonical complete artifact
```

The system-design skill is not guessing which option the interviewer prefers.

It is showing which workload evidence would move you from one design to another.
