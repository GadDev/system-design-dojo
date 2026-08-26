# Day 3 — Optimistic Concurrency & Lost Updates

## Goal

Prevent concurrent actors from silently overwriting each other's decisions without locking the row for the entire user/workflow interaction.

## Timebox

- 15 min — lost update
- 20 min — optimistic locking/version columns
- 15 min — HTTP `ETag` / `If-Match`
- 20 min — transcription state transitions
- 15 min — lab
- 10 min — quiz

---

# 1. The lost-update problem

Two clients read the same state:

```text
Job version = 7
status = PROCESSING
```

Then:

```text
Admin A → CANCEL
Worker B → COMPLETE
```

Naive code:

```sql
UPDATE jobs SET status = 'CANCELLED' WHERE id = 'job-1';
UPDATE jobs SET status = 'COMPLETED' WHERE id = 'job-1';
```

Whichever writes last wins.

That may violate the state machine.

---

# 2. Optimistic concurrency

Optimistic concurrency assumes conflicts are possible but not constant.

Instead of holding a long lock, you update only if the row still has the version you observed.

Schema:

```sql
CREATE TABLE jobs (
    id uuid PRIMARY KEY,
    status text NOT NULL,
    version bigint NOT NULL DEFAULT 0
);
```

Update:

```sql
UPDATE jobs
SET status = 'CANCELLED',
    version = version + 1
WHERE id = :job_id
  AND version = :expected_version
  AND status IN ('QUEUED', 'PROCESSING');
```

Then inspect affected rows.

```text
1 row → you won
0 rows → state changed; reload/reconcile
```

This is a compare-and-swap style operation.

---

# 3. Optimistic locking is not PostgreSQL MVCC

PostgreSQL uses MVCC internally to support concurrent transactions.

Your **application version column** is a domain-level conflict-detection mechanism.

Do not conflate:

```text
MVCC snapshot visibility
```

with:

```text
business version / expected state
```

They solve related but different problems.

---

# 4. State-machine guards can be even better

Sometimes you do not need a generic version.

Example:

```sql
UPDATE chunks
SET status = 'SUCCEEDED',
    artifact_key = :artifact_key,
    completed_at = now()
WHERE id = :chunk_id
  AND status = 'RUNNING';
```

This says:

> Only a chunk currently in RUNNING may transition to SUCCEEDED.

For distributed workers, combining:

- status guards,
- unique constraints,
- deterministic artifact keys,
- idempotency keys,
- version numbers,

can be stronger than relying on locks everywhere.

---

# 5. HTTP optimistic concurrency

HTTP already has a useful mechanism.

Server returns:

```http
HTTP/1.1 200 OK
ETag: "job-7"
```

Client later updates:

```http
PATCH /jobs/123
If-Match: "job-7"
```

If the resource changed to version 8, the server rejects the stale mutation rather than silently overwriting newer state.

RFC 9110 explicitly describes `If-Match` as a way to prevent the **lost update** problem.

Typical response:

```http
412 Precondition Failed
```

---

# 6. Optimistic locking vs pessimistic locking

## Optimistic

```text
read
work without exclusive lock
attempt conditional update
retry/resolve conflict if changed
```

Good when:

- conflicts are infrequent,
- operations are short or user-driven,
- holding locks would be expensive.

## Pessimistic

```sql
SELECT ... FOR UPDATE
```

Good when:

- conflicts are likely,
- operation must protect a short critical section,
- blocking is acceptable.

Neither is universally superior.

---

# 7. Example — finalizer race

Two workers both discover all chunks succeeded.

Bad:

```python
if completed == total:
    merge()
```

Better claim:

```sql
UPDATE jobs
SET status = 'MERGING',
    version = version + 1
WHERE id = :job_id
  AND status = 'PROCESSING'
  AND completed_chunks = expected_chunks;
```

Only the transaction that updates one row owns the merge transition.

The merge operation itself should still be idempotent/deterministic because crashes happen after the claim too.

---

# 8. Conflict is not always an error

Suppose worker attempt A writes the same deterministic result as attempt B.

You may decide:

```text
Already SUCCEEDED with same artifact
→ treat duplicate completion as success
```

Whereas:

```text
Already SUCCEEDED with different pipeline_version/artifact
→ investigate conflict
```

Concurrency handling should encode business semantics.

---

# Exercise — versioned job cancellation

Design:

```http
GET /jobs/123
PATCH /jobs/123/cancel
```

Requirements:

- GET returns a version/ETag.
- Cancel requires `If-Match`.
- Worker may complete concurrently.
- Cancellation must not overwrite a job that already completed.

Write:

1. SQL conditional update.
2. HTTP response on conflict.
3. Client behavior after conflict.
4. Audit event emitted after successful cancellation.

---

# Lab

Run:

```bash
python labs/optimistic_locking_demo.py
```

The script starts two concurrent transitions from the same version. Exactly one conditional update wins.

---

# Break it 💥

1. Two workers deliver the same chunk result.
2. Admin cancels while final merge commits.
3. Client retries a stale `If-Match` update.
4. Worker sees version 9, sleeps 30 seconds, then updates after version 12 exists.
5. An API uses a version column but forgets to include it in the `WHERE` clause.

Explain the correct behavior.

---

# Retrieval quiz

1. What is a lost update?
2. How does a version column detect conflicts?
3. What does “0 rows updated” mean in a compare-and-swap update?
4. Why is an application version column not the same thing as MVCC?
5. What problem does HTTP `If-Match` solve?
6. When might `SELECT ... FOR UPDATE` be preferable?
7. Why should the merge operation remain idempotent even after an atomic merge claim?
8. Give one example where a duplicate completion should be treated as success rather than failure.

## Exit criterion

You can protect a distributed state transition without a giant global lock.
