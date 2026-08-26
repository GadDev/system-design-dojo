# Week 11 — Answer Key / Review Notes

Do the quiz first.

## Selected answers

1. Requirements determine which architecture is appropriate; otherwise the design solves an invented problem.
2. Functional = behavior/capability. Non-functional = quality/constraint such as latency, scale, availability or consistency.
4. Scope exclusions protect time and make assumptions explicit.
8. `requests/day ÷ 86,400`.
10. `total QPS × miss ratio`.
12. Approximate average concurrency (Little's-Law-style intuition).
15. It separates acceptance from completion for asynchronous work.
16. Either the operation is naturally idempotent or the API provides an idempotency/deduplication mechanism.
17. Queries and writes determine indexes, shape and ownership more reliably than generic entity lists.
19. `UNIQUE(job_id, chunk_index, pipeline_version)` is one example.
22. Every extra component adds failure/operational cost; add complexity when requirements justify it.
25. More API replicas can open more DB connections and increase pressure on the real bottleneck.
27. Arrival rate from processing rate and producer lifecycle from consumer lifecycle.
28. So multi-GB bytes do not consume API CPU/memory/network capacity unnecessarily.
29. “What resource/metric is actually saturated?”
32. A single key still maps to one shard/owner unless additional techniques distribute that item's load.
33. API scale often follows request concurrency/RPS; workers follow backlog age/throughput/processing duration/provider limits.
36. A measurable condition that would cause you to revisit the choice.
37. Treat it as a new requirement and adapt, rather than defending the initial diagram.
39. Failure, security/privacy, observability and cost.

## Question 34 example

> “At our current scale we need a durable work queue with at-least-once delivery but not long-term replay. I would start with RabbitMQ/Redis Streams because it is operationally simpler for this workload, and revisit Kafka if event retention, independent replaying consumers or partitioned stream processing become requirements.”

## Question 40

You make assumptions visible, keep the conversation structured, connect decisions to requirements, adapt to feedback and manage time without requiring the interviewer to rescue the session.
