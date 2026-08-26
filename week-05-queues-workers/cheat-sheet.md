# Week 5 Cheat Sheet — Queues & Workers ⚙️

## Core flow

```text
Producer → Broker/Queue → Consumer/Worker
```

For transcription:

```text
FastAPI → Queue → Worker → PostgreSQL/R2
```

---

## Why async?

```text
request latency ≠ job duration
```

Return:

```http
202 Accepted
```

Then expose durable job status separately.

---

## Producer

Creates/publishes work.

## Consumer

Receives messages.

## Worker

Runs business computation.

## ACK

Signals completed responsibility for a delivery.

---

# Delivery semantics

## At-most-once

```text
possible loss
no intentional redelivery
```

## At-least-once

```text
redelivery possible
consumer must tolerate duplicates
```

## Effectively once

```text
at-least-once delivery
+
idempotent business effect
```

## Exactly once

Always ask:

```text
exactly once within what boundary?
```

---

# ACK timing

Safer default for durable work:

```text
receive
process
persist durable result
ACK
```

This implies duplicate-delivery risk.

Therefore:

```text
ACK-after-persist
→ idempotency required
```

---

# Idempotency

Tools:

```text
stable operation ID
unique DB constraint
conditional state transition
processed-message/inbox table
provider idempotency key
```

Example:

```sql
UPDATE jobs
SET status='processing'
WHERE id=:job_id
  AND status='queued';
```

---

# Dual-write problem

```text
DB commit
then
broker publish
```

Crash between them can split state.

## Outbox

```text
DB transaction:
  business row
  + outbox event

later:
  publisher → broker
```

Outbox improves reliable publication intent.

It does **not** remove duplicate publication risk.

---

# Redis Streams

```text
XADD
XREADGROUP
XPENDING
XACK
XAUTOCLAIM
```

Mental model:

```text
append → consumer group → pending → ack/reclaim
```

---

# RabbitMQ

```text
Producer
   ↓
Exchange
   ↓
Queue
   ↓
Consumer
```

Important:

```text
publisher confirm ≠ consumer ACK
prefetch limits in-flight deliveries
DLX routes dead-lettered messages
```

---

# Kafka

```text
Topic
 ├── Partition 0
 ├── Partition 1
 └── Partition N
```

Consumer group:

```text
one active consumer owns a partition at a time within the group
```

Ordering:

```text
within partition
```

Offsets enable replay/reprocessing.

---

# Retry policy

```text
classify failure
↓
retry only if safe/useful
↓
exponential backoff
↓
jitter
↓
max attempts / max age
↓
DLQ or permanent failure
```

---

# Poison message

```text
same work repeatedly fails because of content/state
```

Do not loop forever.

---

# DLQ

A DLQ needs:

```text
owner
alert
retention
inspection
redrive procedure
rate-limited recovery
```

A DLQ nobody watches is a data attic.

---

# Queue metrics

```text
publish rate
queue depth
oldest message age
completion rate
processing p95/p99
pending/in-flight count
redelivery rate
retry rate
DLQ rate
consumer count
```

Most important question:

```text
arrival rate > completion rate ?
```

If yes for long enough:

```text
backlog grows
```

---

# Queue wait is user latency

```text
user completion latency =
upload
+ queue wait
+ processing
+ finalization
```

---

# Message payload

Prefer:

```json
{
  "message_id": "...",
  "job_id": "...",
  "upload_id": "...",
  "schema_version": 1
}
```

Avoid:

```text
huge media bodies
credentials
unnecessary PII
```

---

# Broker selection questions

```text
Need replay?
Need routing?
Need long retention?
Many independent subscribers?
Per-message ACK/requeue?
Ordering scope?
Expected throughput?
Operational maturity?
Already running Redis?
```

---

# Five crash windows to know cold

```text
1. DB commit → crash before publish
2. Publish → response lost → client retries
3. Receive → worker dies before processing
4. Persist result → crash before ACK
5. External side effect succeeds → response/DB update fails
```

If you can explain all five, Week 5 is landing.
