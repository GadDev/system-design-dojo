# Day 5 — Event-Driven Architecture & Consistency

## Goal

Understand how events decouple producers and consumers while introducing **eventual consistency, ordering, duplication, schema evolution and observability** concerns.

## Timebox

- 15 min — event vs command
- 20 min — pub/sub vs work queue
- 20 min — event-driven consistency
- 15 min — outbox/projections
- 20 min — ordering & schemas
- 10 min — quiz

---

# 1. Event vs command

## Command

An instruction expressing intent:

```text
TranscribeChunk
CancelJob
GenerateInvoice
```

Usually there is an intended handler.

## Event

A statement about something that already happened:

```text
ChunkTranscribed
JobCancelled
InvoiceGenerated
```

Events should normally be phrased in the past tense because the fact has already occurred.

This difference matters.

A consumer cannot “reject” the historical truth that `JobCancelled` happened. It can fail to process the event, but the fact remains.

---

# 2. Queue vs publish-subscribe

## Work queue

```text
TranscribeChunk
      ↓
Queue
 ├── worker A
 ├── worker B
 └── worker C
```

One logical worker handles the task.

## Publish-subscribe/event stream

```text
JobCompleted
    ↓
Broker
 ├── Email consumer
 ├── Analytics consumer
 ├── Billing consumer
 └── Search consumer
```

Multiple independent consumers react.

This is why “message queue” and “event-driven architecture” are related but not identical ideas.

---

# 3. Event-driven architecture creates consistency windows

Suppose:

```text
PostgreSQL:
job = COMPLETED
```

Then the outbox publishes:

```text
JobCompleted
```

Consumers update:

```text
Search index
Analytics projection
Notification status
```

Those projections update at different times.

For a while:

```text
DB              COMPLETED
Search          old
Analytics       old
Email           not sent yet
```

This is expected eventual consistency **if the contract permits it**.

---

# 4. The outbox keeps event publication tied to committed state

Within one PostgreSQL transaction:

```sql
BEGIN;

UPDATE jobs
SET status = 'COMPLETED'
WHERE id = :job_id;

INSERT INTO outbox_events (
    event_id,
    aggregate_id,
    event_type,
    payload
) VALUES (...);

COMMIT;
```

A separate publisher sends committed outbox rows to the broker.

This avoids:

```text
DB commit ✅
event publish lost ❌
```

But the publisher may publish twice after an uncertain broker acknowledgement.

Therefore consumers remain idempotent.

---

# 5. Ordering is scoped

Avoid assuming a global order across all distributed events.

Often you only need order **per aggregate/job**.

Example event metadata:

```json
{
  "event_id": "evt-123",
  "aggregate_id": "job-42",
  "aggregate_version": 17,
  "event_type": "ChunkCompleted",
  "schema_version": 2
}
```

Consumer sees:

```text
version 17
then version 16
```

It can detect stale/out-of-order delivery.

Possible reactions:

- ignore duplicate/older event,
- buffer briefly,
- fetch authoritative state,
- retry later.

---

# 6. Idempotent consumer / inbox

Consumer table:

```sql
CREATE TABLE processed_events (
    consumer_name text NOT NULL,
    event_id uuid NOT NULL,
    processed_at timestamptz NOT NULL,
    PRIMARY KEY (consumer_name, event_id)
);
```

Within the consumer's local transaction:

```text
check/insert event id
apply local projection change
commit
ACK broker
```

Duplicate event delivery then becomes harmless.

---

# 7. Event payload: notification vs state transfer

Small notification:

```json
{
  "type": "JobCompleted",
  "job_id": "123",
  "version": 22
}
```

Consumer then fetches authoritative state.

Pros:

- smaller contracts,
- one authority,
- easier correction.

Cons:

- extra read dependency,
- slower processing,
- producer state might have changed again.

Full state transfer:

```json
{
  "type": "JobCompleted",
  "job_id": "123",
  "duration_s": 5420,
  "language": "fr",
  "transcript_key": "...",
  "...": "..."
}
```

Pros:

- consumer can act without read-back.

Cons:

- contract size,
- duplication,
- privacy risk,
- stale copied data,
- schema evolution complexity.

---

# 8. Schema evolution

Producers and consumers deploy independently.

Include:

```text
schema_version
stable event_type
correlation_id / trace context
aggregate_id
aggregate_version
```

Prefer additive evolution where possible.

A consumer should have a defined policy for unknown/new fields and unsupported major versions.

---

# 9. Event-driven architecture does not remove transactions

It changes transaction boundaries.

Each service still uses local transactions:

```text
Service A local transaction
        ↓ event
Service B local transaction
        ↓ event
Service C local transaction
```

The overall workflow becomes eventually consistent.

That means failure handling is part of the architecture, not an afterthought.

---

# Exercise — design `ChunkCompleted`

Define an event with:

```text
event_id
job_id
chunk_id
chunk_index
aggregate_version
pipeline_version
artifact_key
schema_version
occurred_at
trace/correlation context
```

Then answer:

1. Which fields are business facts?
2. Which fields are observability metadata?
3. Which consumer needs the artifact key?
4. Should transcript text itself be in the event?
5. What happens if version 12 arrives before version 11?
6. What happens if event 12 is delivered twice?

---

# Break it 💥

1. Outbox publisher sends an event twice.
2. Consumer updates projection but crashes before ACK.
3. Consumer receives version 21 before 20.
4. Old consumer doesn't understand schema v3.
5. Sensitive transcript text is accidentally copied into five event topics.
6. Search projection is two minutes behind while DB is correct.

Which are acceptable? Which require repair?

---

# Retrieval quiz

1. Command vs event?
2. Work queue vs pub/sub?
3. Why does EDA often produce eventual consistency?
4. What does the outbox solve?
5. Why are consumers still idempotent with an outbox?
6. Why prefer per-aggregate ordering over global ordering when sufficient?
7. What is an inbox/processed-event table?
8. Give one tradeoff between event notification and event-carried state transfer.

## Exit criterion

You can introduce an event without pretending it creates synchronous atomic state everywhere.
