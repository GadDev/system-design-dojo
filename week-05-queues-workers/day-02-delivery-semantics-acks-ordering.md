# Day 2 — Delivery Semantics, Acknowledgements & Ordering

## Goal

Understand the failure windows behind at-most-once, at-least-once, and exactly-once claims, and learn where acknowledgement belongs in a worker lifecycle.

## Timebox

- 20 min — delivery semantics
- 20 min — acknowledgement timing
- 15 min — ordering/prefetch
- 15 min — failure-window exercise
- 10 min — retrieval quiz

---

# 1. Distributed systems live in uncertain windows

Consider:

```text
Worker receives job
Worker transcribes video
Worker writes transcript
Worker sends ACK
```

Now imagine the process crashes **between any two lines**.

Your delivery guarantee is really a set of decisions about these crash windows.

---

# 2. At-most-once

Mental model:

```text
message may be lost
message is not intentionally redelivered
```

A typical risky pattern:

```text
receive
ACK immediately
process
```

If the worker crashes after the ACK but before processing finishes:

```text
broker thinks done
business work never completed
```

Useful when loss is acceptable and duplication is not worth the cost.

Examples might include some telemetry or ephemeral signals—not your user's paid transcription job.

---

# 3. At-least-once

Mental model:

```text
message should eventually be processed
but duplicate delivery can happen
```

Pattern:

```text
receive
process
persist durable effect
ACK
```

Crash window:

```text
persist durable effect ✅
process crashes ❌
ACK never reaches broker
```

Broker redelivers.

Now the same work may execute twice.

Therefore:

> **At-least-once delivery requires duplicate-safe processing.**

This is why Day 3 is entirely about idempotency.

RabbitMQ's reliability guidance explicitly warns that redelivery can occur after connection or acknowledgement failures and recommends idempotent consumers.

Redis Streams consumer groups similarly keep unacknowledged entries pending until they are acknowledged or reclaimed.

---

# 4. “Exactly once” needs a scope

The phrase sounds simple:

```text
process every message exactly once
```

But what exactly counts as “process”?

Suppose a worker:

1. charges a credit card,
2. writes PostgreSQL,
3. publishes another message.

Those are three separate systems.

A broker cannot magically make an arbitrary external API call and a database commit atomically once.

A better question is:

> **Exactly once within which transactional boundary?**

Kafka, for example, supports transactional guarantees for Kafka records and consumer offsets when used correctly. That does not mean arbitrary side effects outside Kafka become magically exactly-once.

For application design, a useful target is often:

> **At-least-once delivery + idempotent processing = effectively-once business effect.**

---

# 5. When should a worker ACK?

For durable business work, usually only after the durable state transition you care about.

Example:

```text
receive
 ↓
validate job
 ↓
perform transcription
 ↓
store transcript
 ↓
UPDATE jobs SET status='completed'
 ↓
ACK
```

If ACK comes before durable completion, you create a loss window.

If ACK comes after durable completion, you create a duplicate-delivery window.

The second is generally safer **if the worker is idempotent**.

---

# 6. Producer acknowledgements matter too

There are two different questions:

```text
Did broker accept my publish?
Did consumer finish my message?
```

They are not the same acknowledgement.

RabbitMQ distinguishes:

- **publisher confirms** — broker accepted responsibility,
- **consumer acknowledgements** — consumer finished responsibility.

Failure scenario:

```text
Producer sends message
network breaks
Producer does not receive confirm
```

Did the broker store it?

Maybe.

Producer retries.

Duplicate publication is possible.

Again: idempotency.

---

# 7. Prefetch / in-flight work

Suppose a worker can process only two videos concurrently but receives 500 unacknowledged messages.

That creates:

- memory pressure,
- poor fairness,
- long hidden in-flight delays,
- slow recovery if worker dies.

RabbitMQ exposes **prefetch** to limit outstanding unacknowledged deliveries.

Conceptually:

```text
prefetch = 4
```

means the broker should not flood that consumer with unlimited work.

This connects directly to Week 4 backpressure.

---

# 8. Ordering is usually narrower than you think

Suppose messages arrive:

```text
1, 2, 3, 4
```

With four workers:

```text
worker A finishes 3 first
worker B finishes 1 second
worker C finishes 4 third
worker D finishes 2 last
```

Queue delivery order does not imply completion order.

Ask:

> What must actually be ordered?

For transcription jobs belonging to unrelated videos:

```text
probably nothing globally
```

For state transitions of the same job:

```text
maybe yes
```

Kafka provides ordering within a partition, not across an entire multi-partition topic.

Redis Streams have ordered IDs but parallel consumers can still complete work in a different order.

RabbitMQ can dequeue in order, while parallel consumers/redeliveries can affect observed processing order.

The senior answer is not “my broker guarantees FIFO.”

It is:

> **What business invariant depends on ordering, and at what key/partition scope?**

---

# 9. Failure-window table

Fill this before reading the hints.

| Crash point | Possible result | What protects us? |
|---|---|---|
| Before message publish | Job exists but no message | ? |
| After publish, before HTTP response | Client may retry creation | ? |
| After receive, before processing | Delivery unfinished | ? |
| After DB completion, before ACK | Duplicate delivery | ? |
| After ACK, before DB completion | Lost work | ? |

Hints live in Days 3 and 6.

---

# 10. Exercise — choose delivery semantics

Choose a reasonable guarantee and justify it for:

1. Page-view analytics.
2. Billing transaction.
3. User transcription job.
4. Email notification.
5. Cache invalidation event.
6. “video upload completed” workflow event.

Avoid using “exactly once” until you define the exact boundary.

---

# 11. Break it 💥

A worker performs:

```text
1. receive job_123
2. call transcription provider
3. provider completes and charges you
4. save transcript
5. ACK
```

It crashes after step 3.

The broker redelivers.

Questions:

- Can the provider request be retried safely?
- Does the provider support idempotency keys?
- Can you detect an existing provider operation?
- What is your durable state before making the external call?
- Is automatic retry actually safe here?

This is why “retry 3 times” is not a complete failure policy.

---

# Retrieval quiz

1. Define at-most-once.
2. Define at-least-once.
3. Why does ACK-after-processing imply possible duplicates?
4. Why does ACK-before-processing imply possible loss?
5. What is a publisher confirm?
6. What does consumer prefetch protect against?
7. Why is global ordering expensive or unnecessary in many workloads?
8. What does Kafka order: a topic globally or a partition?
9. What does “effectively once” usually mean in application architecture?
10. Why is “exactly once” incomplete without a scope?

## Exit criterion

You can draw every crash window around receive → process → persist → ACK and explain what guarantee each ordering creates.
