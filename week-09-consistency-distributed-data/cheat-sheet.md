# Week 9 — Consistency Cheat Sheet 🥋

## Consistency is per fact / operation

```text
What must be true?
How fresh must reads be?
What happens when nodes cannot coordinate?
```

## Strong consistency

Reads/writes behave according to a stronger single-authoritative-order contract.

Cost often includes:

```text
coordination ↑
latency ↑
availability under partition ↓
```

## Eventual consistency

Derived copies may temporarily disagree but are expected to converge.

Always define:

```text
max/target lag
repair path
user-visible behavior
```

## Useful client guarantees

```text
read-your-writes
monotonic reads
bounded staleness
per-aggregate ordering
```

## CAP

During a network partition:

```text
preserve stronger consistency
→ may reject/defer requests

preserve availability
→ may accept divergent/stale state
```

Do not just say “pick two.”

## Replica lag

```text
Primary v42
Replica v41
```

Can break:

```text
read-your-writes
monotonic reads
fresh authorization decisions
```

## Optimistic concurrency

```sql
UPDATE jobs
SET status = 'CANCELLED',
    version = version + 1
WHERE id = :id
  AND version = :expected_version;
```

```text
1 row → success
0 rows → conflict/reload
```

HTTP equivalent:

```text
ETag
If-Match
412 Precondition Failed
```

## Local transaction

```text
one transactional resource
→ ACID is easy(er)
```

## Distributed transaction

```text
multiple independent transactional resources
→ coordination required
```

## 2PC

```text
PREPARE all
   ↓
COMMIT all / ROLLBACK all
```

Risk:

```text
prepared state
locks/resources retained
coordinator recovery required
```

## Saga

```text
local tx A
 ↓
local tx B
 ↓ failure
compensate B/A as business actions
```

## Event

Past-tense fact:

```text
JobCompleted
ChunkTranscribed
```

## Command

Intent:

```text
TranscribeChunk
CancelJob
```

## Transactional outbox

```text
business state + event intent
same DB transaction
```

Still requires idempotent publisher/consumer.

## Inbox / processed events

```text
(consumer_name, event_id) UNIQUE
```

Prevents duplicate business effect.

## Source of truth

Define authority **per fact**:

```text
workflow state        → PostgreSQL
artifact bytes        → R2
delivery state        → broker
cache/search/analytics→ derived
```

## Retry vs reconciliation

```text
Retry
→ immediate attempt to finish operation

Reconciliation
→ compare durable systems later and repair divergence
```

## Strong invariants

```text
one logical chunk result per version
SUCCEEDED → valid artifact
MERGING only when all required chunks accepted
COMPLETED → final artifact exists
billing event cannot double-charge
```

## Senior questions

```text
What fact are we protecting?
Who owns that fact?
Which copies are derived?
What conflict can occur?
How is conflict detected?
What can be stale?
How do we converge?
What does the user observe during divergence?
```
