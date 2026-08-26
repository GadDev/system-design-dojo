# Week 5 — Sources & Reading Map 📚

This week uses **official documentation first**, then books and worked examples.

The goal is not to memorize broker configuration. The goal is to understand the guarantees each system exposes and the failure windows your application must handle.

---

# Reading rule

For every source, finish with this sentence:

> “This mechanism protects me from ___, but it does not protect me from ___.”

That one habit prevents a lot of magical thinking around messaging.

---

# Day 1 — Queues, producers, consumers, workers

## FastAPI — Background Tasks

Official:

- https://fastapi.tiangolo.com/tutorial/background-tasks/

Read especially the **Caveat** section.

Why:

FastAPI explicitly distinguishes small same-process background work from heavier jobs that benefit from a separate task queue and workers across processes/servers.

Questions:

- What happens to a same-process background task if the process dies?
- Why is a 60–120 minute transcription job different from sending a small notification?

## RabbitMQ — Consumers

- https://www.rabbitmq.com/docs/consumers

Focus:

- consumer lifecycle,
- acknowledgements,
- prefetch,
- connection failure recovery.

## Redis — Streams use case

- https://redis.io/docs/latest/develop/use-cases/streaming/

Focus:

- producer,
- consumer group,
- pending work,
- acknowledgement.

---

# Day 2 — Delivery semantics & acknowledgements

## RabbitMQ — Reliability Guide

- https://www.rabbitmq.com/docs/reliability

Read:

- acknowledgements and confirms,
- publisher failure windows,
- consumer redelivery,
- data safety responsibilities.

Important question:

> What happens if the broker sent a publisher confirm but the producer never received it?

That is where duplicates are born.

## RabbitMQ — Queues

- https://www.rabbitmq.com/docs/queues

Focus:

- manual vs automatic acknowledgement,
- prefetch,
- durability.

## Apache Kafka — Design / delivery semantics

- https://kafka.apache.org/41/design/design/

Focus:

- at-most-once,
- at-least-once,
- exactly-once scope,
- consumer offsets,
- producer transactions.

Do not turn “Kafka supports exactly-once” into “every arbitrary side effect in my application happens exactly once.”

---

# Day 3 — Idempotency & durable publication

## RabbitMQ Reliability Guide — redelivery

- https://www.rabbitmq.com/docs/reliability

Focus on why applications must tolerate duplicate deliveries.

## PostgreSQL from Week 2

Revisit:

- unique constraints,
- transactions,
- conditional updates,
- isolation/concurrency.

These are your main tools for implementing idempotent business effects.

## Transactional Outbox pattern

Good conceptual reference:

- https://microservices.io/patterns/data/transactional-outbox.html

Treat this as a pattern reference, not a standard.

Key question:

> Why can an outbox solve “DB committed but message intent disappeared” while still allowing duplicate publication?

---

# Day 4 — Redis Streams, RabbitMQ, Kafka

## Redis Streams

- https://redis.io/docs/latest/develop/data-types/streams/
- https://redis.io/docs/latest/develop/use-cases/streaming/
- https://redis.io/docs/latest/commands/xpending/
- https://redis.io/docs/latest/commands/xautoclaim/

Focus:

```text
XADD
XGROUP
XREADGROUP
XPENDING
XACK
XAUTOCLAIM
```

The command names matter less than the lifecycle:

```text
append → deliver → pending → process → acknowledge → reclaim if abandoned
```

## RabbitMQ

- https://www.rabbitmq.com/docs/consumers
- https://www.rabbitmq.com/docs/publishers
- https://www.rabbitmq.com/docs/dlx
- https://www.rabbitmq.com/docs/quorum-queues

Focus:

- exchanges vs queues,
- confirms vs ACKs,
- prefetch,
- dead-lettering,
- replicated queue tradeoffs.

## Apache Kafka

- https://kafka.apache.org/documentation/
- https://kafka.apache.org/41/design/design/

Focus:

- topics,
- partitions,
- consumer groups,
- offsets,
- replay,
- ordering within a partition.

Core exercise:

> Why does adding consumers beyond the partition count not keep increasing active consumption parallelism inside one group?

---

# Day 5 — Retry and dead-letter behavior

## RabbitMQ — Dead Letter Exchanges

- https://www.rabbitmq.com/docs/dlx

Understand what can cause dead-lettering and why a DLQ must have an operational owner.

## Celery — Tasks and Retry

- https://docs.celeryq.dev/en/stable/userguide/tasks.html

Focus:

- retry,
- max retries,
- exponential backoff,
- jitter.

Framework syntax is secondary. Extract the general failure policy.

## Google SRE — cascading failures

- https://sre.google/sre-book/addressing-cascading-failures/

Connect this to retry storms.

Ask:

> How can a correct local retry decision create a global outage when thousands of workers do it simultaneously?

---

# Day 6 — Production transcription pipeline

## FastAPI BackgroundTasks caveat

Re-read:

- https://fastapi.tiangolo.com/tutorial/background-tasks/

You should now be able to explain **why** a multi-server queue/worker model is justified for this workload.

## Celery overview

- https://docs.celeryq.dev/en/stable/getting-started/introduction.html

Use it as an example of a Python task framework layered over a broker.

Ask:

- Which concepts belong to Celery?
- Which belong to Redis/RabbitMQ underneath?
- What happens if you swap the broker?

---

# Books

## Designing Data-Intensive Applications, 2nd Edition

Use as the conceptual spine.

Week 5 topics to focus on:

- dataflow through services,
- message passing,
- logs/streams,
- retries and fault tolerance,
- consistency around distributed state.

Do not try to read the entire book this week.

## Enterprise Integration Patterns — Gregor Hohpe & Bobby Woolf

Classic vocabulary for messaging patterns.

Useful concepts:

- message channel,
- competing consumers,
- dead letter channel,
- idempotent receiver,
- message router.

The technology examples are older; the patterns remain useful.

## Designing Event-Driven Systems — Ben Stopford

Useful for understanding event logs, streams, Kafka-style architecture, and why event retention/replay changes the model.

## Release It! — Michael Nygard

Useful for retries, stability boundaries, bulkheads, timeouts, and failure amplification.

---

# Optional deeper dives

## RabbitMQ quorum queues

Read only after you understand a normal queue:

- https://www.rabbitmq.com/docs/quorum-queues

Question:

> What availability/durability problem justifies replication overhead?

## Kafka transactions

Read only after at-least-once is intuitive:

- https://kafka.apache.org/41/design/design/

Question:

> What exact state can Kafka transactions coordinate atomically, and what external side effects remain outside that boundary?

## Redis reclaiming abandoned work

- https://redis.io/docs/latest/commands/xautoclaim/

Question:

> How do you distinguish a slow consumer from a dead consumer before reclaiming work?

---

# Do not start with comparison blogs

Search-result articles titled:

```text
Redis vs RabbitMQ vs Kafka: WHICH IS BEST???
```

are often optimized for clicks rather than requirements. 😄

Build your own selection matrix first.

Then use external comparisons as critique material.

---

# Week 5 source hierarchy

```text
1. Official broker/framework docs
2. PostgreSQL/system-design knowledge from earlier weeks
3. SRE reliability material
4. Architecture pattern references
5. Books
6. Worked interview examples
```

That order keeps implementation details anchored to actual guarantees.
