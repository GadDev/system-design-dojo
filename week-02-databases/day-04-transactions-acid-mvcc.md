# Day 4 — Transactions, ACID, MVCC & Isolation

## Goal

Understand how PostgreSQL keeps multi-step operations correct under concurrency—and why "we used a transaction" still does not automatically make business logic safe.

## Timebox

- 15 min — transaction mental model
- 20 min — ACID
- 20 min — MVCC and isolation
- 20 min — job state exercise
- 10 min — deadlocks/retries
- 10 min — retrieval quiz

---

# 1. Transaction = one logical unit of work

Suppose completing a chunk requires:

```text
1. store chunk text
2. mark chunk DONE
3. increment job completed_chunks
```

Without a transaction:

```text
step 1 succeeds
step 2 succeeds
process crashes
step 3 never happens
```

Now data is inconsistent.

With a transaction:

```sql
BEGIN;

UPDATE chunks ...;
UPDATE jobs ...;

COMMIT;
```

Either the unit commits or it is rolled back.

---

# 2. ACID

## Atomicity

All operations in the transaction succeed as one logical unit or none become committed effects.

Think:

```text
all or nothing
```

## Consistency

A successful transaction takes the database from one valid state to another, according to the constraints/invariants the system enforces.

Examples:

```text
FK remains valid
UNIQUE remains valid
completed_chunks <= total_chunks
```

Important nuance:

The database does not magically know every business rule. You have to encode rules with constraints, transactions, locks, or application logic.

## Isolation

Concurrent transactions should not observe/produce invalid interference beyond what the chosen isolation level allows.

## Durability

After commit, PostgreSQL is designed to preserve committed changes across crashes through its durability mechanisms (notably WAL).

---

# 3. Autocommit

By default, PostgreSQL treats each statement as its own transaction if you do not explicitly start a transaction block.

So:

```sql
UPDATE chunks ...;
UPDATE jobs ...;
```

is not automatically one atomic unit.

You need:

```sql
BEGIN;
...
COMMIT;
```

when several statements together express one invariant.

---

# 4. MVCC: multiple versions, fewer read/write conflicts

PostgreSQL uses **Multi-Version Concurrency Control (MVCC)**.

Mental model:

```text
Transaction A sees snapshot S1
Transaction B updates rows
Transaction A can often continue reading its snapshot
```

This lets readers and writers coexist with much less blocking than a simplistic "one global lock" model.

But MVCC does not mean:

```text
no locks
no anomalies
no conflicts
```

PostgreSQL still uses row/table locks where needed, and isolation level matters.

---

# 5. Isolation levels

PostgreSQL implements three distinct behaviors for the standard levels:

```text
Read Committed   ← default
Repeatable Read
Serializable
```

(`Read Uncommitted` behaves like Read Committed in PostgreSQL.)

## Read Committed

Each statement sees a snapshot appropriate to that statement.

Two SELECTs in one transaction can see different committed data if another transaction commits between them.

Good default for many applications.

## Repeatable Read

The transaction sees a stable snapshot.

Useful when you want consistent repeated reads, but concurrency conflicts can still require care.

## Serializable

PostgreSQL attempts to make committed concurrent transactions behave as if they executed serially in some order.

Cost:

- more overhead,
- transactions may fail with serialization errors,
- application must retry the **whole transaction**.

Strong guarantees are not free.

---

# 6. Lost-update style thinking

Imagine two workers process the same job concurrently.

Both read:

```text
completed_chunks = 40
```

Worker A writes:

```text
41
```

Worker B also writes:

```text
41
```

But two chunks completed.

A safer atomic SQL operation is:

```sql
UPDATE jobs
SET completed_chunks = completed_chunks + 1
WHERE id = $1;
```

Even better: make chunk completion idempotent so the same chunk cannot increment twice.

This is where transactions meet application correctness.

---

# 7. Idempotent chunk completion

Suppose a worker retries after an uncertain network failure.

You want:

```text
same chunk completion event twice
             ↓
only one logical completion
```

Possible strategy:

```sql
BEGIN;

UPDATE chunks
SET status = 'done', text = $text
WHERE id = $chunk_id
  AND status <> 'done';

-- only increment parent if the chunk transitioned now

COMMIT;
```

The exact implementation varies.

The principle is:

> Retrying infrastructure and transaction semantics must agree on what "already applied" means.

---

# 8. Savepoints

Savepoints let you partially roll back within a larger transaction.

```sql
BEGIN;

INSERT ...;
SAVEPOINT before_optional_step;

-- operation fails
ROLLBACK TO SAVEPOINT before_optional_step;

COMMIT;
```

Useful, but do not turn transactions into 20-minute workflow containers.

Long transactions can:

- hold resources,
- retain row versions,
- increase contention,
- interfere with maintenance.

---

# 9. Deadlocks

Two transactions can each hold something the other needs.

```text
Tx A locks Job 1
Tx B locks Job 2
Tx A waits for Job 2
Tx B waits for Job 1
```

PostgreSQL detects deadlocks and aborts one transaction.

Mitigations include:

- consistent lock ordering,
- short transactions,
- retry logic.

A deadlock is not necessarily a database bug. It can be an application concurrency design issue.

---

# Exercise — Safe job completion

Design one transaction that marks a job complete only when every chunk is done.

Requirements:

- no duplicate chunk count,
- final transcript row created once,
- job transitions `processing → completed` once,
- a retry after timeout is safe.

Write:

```text
Invariant:
Transaction steps:
Constraint(s):
Possible race:
Retry behavior:
```

Then consider two workers attempting the final transition simultaneously.

What prevents two transcript rows?

Hint:

```text
UNIQUE(job_id)
```

can turn a concurrency assumption into a database-enforced invariant.

---

# Break it 💥

What happens if:

1. A worker crashes before COMMIT?
2. A worker crashes after COMMIT but before receiving the response?
3. Two workers finalize the same job simultaneously?
4. A transaction runs for 45 minutes?
5. A SERIALIZABLE transaction gets a serialization failure?

---

# Retrieval quiz

1. What problem does a transaction solve?
2. Define ACID in your own words.
3. Does "Consistency" mean the database knows all product rules automatically?
4. What is PostgreSQL autocommit?
5. What does MVCC buy us?
6. What is PostgreSQL's default isolation level?
7. Why can SERIALIZABLE require retries?
8. Why is `SET x = x + 1` safer than read-then-write for counters?
9. What is a deadlock?
10. Why should transactions usually be short?

## Exit criterion

You can identify the invariant a transaction protects, describe concurrency risks, and explain how retries interact with transactional correctness.
