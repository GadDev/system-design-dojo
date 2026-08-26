# Week 5 Review & Retrieval Quiz 🥷

## Rules

Do this **without notes** first.

- 40 questions
- 1 point each
- Explain aloud where possible
- Do not open `answer-key.md` until the first attempt is complete

---

# Part 1 — Async mental model

1. Why is keeping `POST /transcribe` open for 38 minutes a poor default architecture?
2. What does a queue decouple?
3. Define producer.
4. Define consumer.
5. Define worker.
6. What does `202 Accepted` communicate?
7. Why should large media usually not be placed inside queue messages?
8. What is the difference between queue depth and oldest-message age?

---

# Part 2 — Delivery semantics

9. Define at-most-once delivery.
10. Define at-least-once delivery.
11. Why does ACK-after-persist still allow duplicate delivery?
12. Why does ACK-before-persist create a loss window?
13. What does “effectively once” usually mean at application level?
14. Why is “exactly once” meaningless without a scope/boundary?
15. What is the difference between a RabbitMQ publisher confirm and consumer acknowledgement?
16. What problem does prefetch/in-flight limiting solve?

---

# Part 3 — Idempotency

17. Define an idempotent business operation.
18. How can a database unique constraint help with duplicate processing?
19. Why are conditional state transitions useful?
20. Give an example of a stable idempotency key for a transcription request.
21. What is the dual-write problem?
22. What does a transactional outbox solve?
23. Why can an outbox publisher still publish the same event twice?
24. What is an inbox/processed-message table for?

---

# Part 4 — Redis, RabbitMQ, Kafka

25. What does `XACK` mean in Redis Streams?
26. What is the Redis Streams pending entries list?
27. What is `XAUTOCLAIM` useful for?
28. In RabbitMQ, what role does an exchange play?
29. What is a dead-letter exchange/path used for?
30. In Kafka, what is a consumer offset?
31. What is the unit of active consumer-group parallelism in Kafka?
32. Where does Kafka provide ordering guarantees?

---

# Part 5 — Retries & operations

33. Difference between transient and permanent failure?
34. Why use exponential backoff?
35. Why add jitter?
36. What is a poison message?
37. Why does a DLQ need an owner and redrive policy?
38. Why can replaying an entire DLQ at once cause another outage?
39. Name five metrics you would put on a queue/worker dashboard.
40. What happens over time if job arrival rate stays above total worker completion rate?

---

# Architecture reconstruction

Without previous diagrams, draw:

```text
React
 ↓
Load Balancer
 ↓
FastAPI replicas
 ↓
PostgreSQL + Outbox
 ↓
Publisher
 ↓
Queue
 ↓
Worker Pool
 ↓
R2 / PostgreSQL
```

Add:

```text
DLQ
ACK
retry path
GET /jobs/{id}
```

Then annotate the exact place where:

- user job becomes durable,
- broker takes ownership,
- worker takes responsibility,
- durable processing completes,
- message is acknowledged.

---

# Failure defense

Explain what happens when:

### Scenario A

PostgreSQL commits job + outbox, broker is unavailable for 30 minutes.

### Scenario B

Worker stores final transcript and updates `COMPLETED`, then crashes before ACK.

### Scenario C

AI provider is returning 503 to all 200 workers.

### Scenario D

One corrupt video has been delivered 16 times.

### Scenario E

Kafka topic has 8 partitions; you deploy 50 consumers in the same group.

### Scenario F

RabbitMQ prefetch is 100 but each task takes 30 minutes.

---

# Oral prompts

Give yourself 2 minutes each.

## Prompt 1

> Why does at-least-once delivery require idempotency?

## Prompt 2

> Redis Streams vs RabbitMQ vs Kafka for the transcription MVP?

## Prompt 3

> Explain the transactional outbox pattern without using jargon as the explanation.

## Prompt 4

> Why can retries make an outage worse?

## Prompt 5

> Queue depth is 20,000. Is the system unhealthy?

Your answer to Prompt 5 should begin with:

> “It depends…”

and then ask about processing time, arrival/completion rates, and oldest-message age.

---

# Score

| Score | Meaning |
|---|---|
| 36–40 | Strong — ready for distributed processing/orchestration |
| 31–35 | Good — review weak crash windows |
| 24–30 | Revisit Days 2–5 |
| <24 | Rebuild the async lifecycle from Day 1 |

The score is not the objective. The objective is being able to explain **why duplicates, retries, and backlog exist** without hand-waving.
