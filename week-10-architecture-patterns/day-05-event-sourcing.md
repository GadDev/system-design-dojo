# Day 5 — Event Sourcing: Store the History Only When the History Is the Product

## Goal

Understand event sourcing as a persistence model where an append-only event stream is authoritative, and recognize why it is powerful, invasive and usually unnecessary.

## Timebox

- 20 min — current state vs event stream
- 25 min — rehydration, projections and snapshots
- 20 min — concurrency and event versions
- 20 min — schema evolution + transcription suitability
- 10 min — break-it drill + quiz

---

## 1. Traditional state storage

Typical job row:

```json
{
  "id": "job_123",
  "status": "COMPLETED",
  "progress": 100,
  "version": 44
}
```

You know the current state.

Unless you add history/audit tables, you may not know exactly how it got there.

---

## 2. Event-sourced state

Instead store facts:

```text
JobCreated
UploadAttached
ProcessingStarted
ChunkCompleted(0)
ChunkCompleted(1)
...
JobCompleted
```

Current state is derived by replaying the stream.

```text
Event stream
   ↓ replay
Aggregate state
```

The event store is authoritative.

---

## 3. Why this can be valuable

Event sourcing can be compelling when:

- complete audit history is a domain requirement,
- the reason/intent behind state changes matters,
- historical reconstruction matters,
- temporal queries are valuable,
- new projections must be built from past behavior,
- domain behavior naturally maps to immutable events.

It is not justified merely because your application already publishes integration events.

---

## 4. Aggregate stream

Example:

```text
stream: job-job_123

1 JobCreated
2 ProcessingStarted
3 ChunkCompleted(0)
4 ChunkCompleted(1)
5 JobCancelled
```

To append version 6, the writer may say:

```text
expected_version = 5
```

If another command already appended version 6, your append fails and the command must re-evaluate.

This gives optimistic concurrency at stream level.

---

## 5. Rehydration cost

A long-lived aggregate could have thousands of events.

Replaying all of them for every command can become expensive.

Use snapshots:

```text
snapshot at version 1000
        ↓
replay events 1001..1044
```

A snapshot is an optimization.

The event stream remains authoritative.

---

## 6. Queries need projections

Event stores are usually poor query databases for UI questions such as:

```text
show my 50 latest failed jobs
```

So event sourcing commonly pairs with projections:

```text
Event Store
   ├──→ JobHistoryProjection
   ├──→ BillingProjection
   └──→ AnalyticsProjection
```

This is one reason Event Sourcing and CQRS are often discussed together.

---

## 7. Event evolution is forever-ish

Once historical events are authoritative, old event schemas matter for years.

Suppose:

```json
{
  "type": "JobCreated",
  "language": "en"
}
```

becomes:

```json
{
  "type": "JobCreated",
  "language": {
    "source": "en",
    "auto_detect": false
  }
}
```

You need strategies such as:

- upcasters,
- tolerant readers,
- versioned event types,
- migration of event data in rare cases.

CRUD schema migration is already work.

Event-sourced history makes evolution a first-class design concern.

---

## 8. Correction is another event

You do not generally rewrite history to “undo” something.

You append a correcting fact:

```text
UsageCharged
UsageChargeReversed
```

This preserves audit history.

It also changes how developers think about updates.

---

## 9. Should the transcription SaaS use event sourcing?

Probably **not globally**.

Current-state PostgreSQL tables are simpler for:

```text
uploads
jobs
chunks
transcripts
```

Possible future bounded use case:

### Billing/usage ledger

If immutable, auditable changes are legally/business critical:

```text
MinutesReserved
MinutesConsumed
CreditGranted
ChargeReversed
```

An append-only ledger style may be valuable.

But even there, a traditional immutable ledger table may satisfy the requirement without full event sourcing.

The question is always:

> What capability do we gain that simpler persistence cannot provide cheaply enough?

---

## 10. Event sourcing ≠ event-driven architecture

An application may publish events while persisting current state.

```text
PostgreSQL current state
+
integration events
```

That is event-driven collaboration, not necessarily event sourcing.

Event sourcing specifically means **events are the authoritative persistence model for that domain state**.

---

## Exercise — Architecture decision

Evaluate event sourcing for:

1. Job lifecycle
2. Chunk processing
3. Billing/usage
4. Audit log
5. User profile

For each score:

```text
history value
replay value
audit requirement
write contention
projection need
schema-evolution cost
team expertise
```

Choose at most one candidate.

“None” is a valid answer.

---

## Break it 💥

1. Event `JobCreatedV1` from four years ago can no longer deserialize.
2. Projection is deleted accidentally.
3. Two writers append against version 42 simultaneously.
4. Aggregate has 2 million events.
5. A developer edits an old event to “fix” history.
6. Integration events are mistaken for the event store.

---

## Retrieval quiz

1. What is authoritative in event sourcing?
2. What is rehydration?
3. Why use snapshots?
4. Why are projections common?
5. How does optimistic concurrency work on a stream?
6. Why is event schema evolution unusually important?
7. Difference between event sourcing and event-driven architecture?
8. Why is event sourcing often overused?

## Exit criterion

You can say **no** to event sourcing for a technically sophisticated reason.
