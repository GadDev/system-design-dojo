# Day 1 — Strong vs Eventual Consistency

## Goal

Learn to express consistency as a **requirement for a specific operation**, rather than saying an entire architecture is simply “strong” or “eventual.”

## Timebox

- 20 min — what consistency means
- 20 min — common consistency requirements
- 20 min — transcription scenarios
- 15 min — exercise
- 10 min — retrieval quiz

---

# 1. Why consistency appears only after distribution

With one authoritative PostgreSQL transaction, reasoning is relatively local:

```text
BEGIN
UPDATE job
INSERT transcript_metadata
COMMIT
```

Either the transaction commits or it does not.

Now distribute the state:

```text
PostgreSQL
R2
Redis
Queue
Read replica
Analytics projection
```

Those components cannot all change atomically by accident.

Temporary disagreement becomes possible.

---

# 2. Strong consistency: useful mental model

For this course, a strongly consistent read means you can reason as if the read observes the latest successfully committed authoritative write required by the contract.

Example:

```text
User cancels job
      ↓
API returns success
      ↓
next authoritative read must not say RUNNING
```

This kind of guarantee may require:

- reading from the primary,
- coordination,
- quorum/consensus in some distributed stores,
- rejecting operations when consistency cannot be guaranteed.

The cost is often latency, coordination or reduced availability under failure.

---

# 3. Eventual consistency

Eventual consistency allows derived copies to lag behind the authoritative state, with the expectation that they converge if updates stop and propagation succeeds.

Example:

```text
PostgreSQL primary:
job.status = COMPLETED

read projection:
job.status = PROCESSING

...event propagates...

projection:
job.status = COMPLETED
```

This can be perfectly acceptable for:

- analytics,
- search indexes,
- dashboard aggregates,
- recommendation feeds,
- non-critical reporting.

It may be unacceptable for:

- billing authorization,
- enforcing a hard quota,
- cancellation ownership,
- deciding whether a destructive operation is permitted.

---

# 4. “Strong vs eventual” is too coarse

Useful guarantees include:

## Read-your-writes

After **you** successfully update a resource, your next read should reflect that update.

```text
PATCH profile
→ 200
GET profile
→ old value  ❌ bad UX
```

## Monotonic reads

Once a client has observed version 8, it should not later observe version 7.

```text
read v8
read v7  ❌ time travel
```

## Consistent prefix / ordering

A consumer should not observe later dependent events without earlier prerequisites.

```text
JobCompleted
before
JobCreated
```

would be nonsensical for many consumers.

## Bounded staleness

A copy may lag, but only within an explicit window.

```text
analytics may be ≤ 5 minutes stale
```

This is more useful than saying “eventually.”

---

# 5. Authority vs freshness

A common mistake:

> “The queue has the newest message, therefore the queue is the source of truth.”

Not necessarily.

Authority is about **which component owns the fact**, not which copy happens to be newer.

For the transcription system:

| Fact | Possible authority |
|---|---|
| job lifecycle state | PostgreSQL |
| immutable chunk artifact bytes | R2 |
| message delivery/pending state | broker |
| cached job response | Redis is derived |
| analytics dashboard | projection is derived |

The queue can prove that a message was delivered/pending/acknowledged according to broker semantics. It does **not automatically prove** that your business transaction completed.

---

# 6. Consistency windows are product decisions

Suppose a job completes at 10:00:00.

Possible contracts:

```text
job details API       → ≤ 1 second stale
history page          → ≤ 10 seconds stale
analytics dashboard   → ≤ 5 minutes stale
billing ledger        → must use authoritative committed facts
```

One application can intentionally use several consistency models.

---

# 7. Apply it to your transcription application

Classify each read:

### A. `GET /jobs/{id}` while user watches progress

Questions:

- Can it be 2 seconds stale?
- Must progress never move backward?
- What happens after cancellation succeeds?

### B. Monthly usage invoice

Questions:

- Can replica lag undercount billable minutes?
- Is this a projection or ledger?
- How do corrections work?

### C. “Recent jobs” list

Could tolerate mild staleness, but read-your-writes might matter immediately after upload.

### D. Transcript search index

Search can often lag behind the authoritative transcript artifact.

---

# 8. Stronger consistency is not automatically better

Stronger guarantees often require more coordination.

More coordination can mean:

```text
latency ↑
availability during failure ↓
operational complexity ↑
```

The question is:

> **What invariant or user expectation requires the stronger guarantee?**

---

# Exercise — Consistency contract matrix

Fill this before reading tomorrow:

| Operation | Authority | Required consistency | Max staleness | Failure behavior |
|---|---|---|---|---|
| create upload | | | | |
| cancel job | | | | |
| job progress | | | | |
| completed transcript fetch | | | | |
| usage/billing | | | | |
| analytics dashboard | | | | |
| search index | | | | |

For every “strong” answer, explain what would break if it were eventually consistent.

For every “eventual” answer, define an acceptable convergence window.

---

# Break it 💥

Imagine:

1. Primary says `COMPLETED`, replica says `PROCESSING`.
2. User cancels a job, then refreshes via a stale replica.
3. Search does not find a transcript for 40 seconds after completion.
4. Billing projection is 3 minutes behind.
5. Redis still has `PROCESSING` after PostgreSQL says `FAILED`.

Which are correctness bugs? Which are acceptable stale reads? Which are UX bugs?

---

# Retrieval quiz

1. What does eventual consistency promise at a high level?
2. Why is “this whole system is eventually consistent” often too vague?
3. Define read-your-writes.
4. Define monotonic reads.
5. What is bounded staleness?
6. Why is the newest copy not automatically the authoritative copy?
7. Give one transcription fact that should have strong authoritative semantics.
8. Give one derived projection that may converge later.

## Exit criterion

You can specify a consistency requirement **per operation/fact** and explain the cost of making it stronger.
