# Week 10 Review & Retrieval Quiz 🧠

Do this without notes first.

## Part 1 — Modular monolith

1. What is the difference between a monolith and a big ball of mud?
2. What makes a monolith modular?
3. Why prefer domain-shaped modules over only technical layers?
4. What is a module's public contract?
5. Why are circular module dependencies dangerous?
6. Can one PostgreSQL database still have logical data ownership?
7. How can internal events help a modular monolith?

## Part 2 — Microservices

8. What does independently deployable mean?
9. Name four benefits microservices can provide.
10. Name five costs of distribution.
11. What is the microservice premium?
12. What is a distributed monolith?
13. Why is “one service per table” usually a bad decomposition rule?
14. Name four evidence-based extraction triggers.
15. Why can extracting too early freeze the wrong domain boundary?

## Part 3 — Event-driven architecture

16. Difference between a command and an event?
17. What does producer/consumer decoupling buy you?
18. Why does EDA often introduce eventual consistency?
19. What does an outbox protect against?
20. Why are idempotent consumers still required?
21. Why should integration events avoid leaking persistence internals?
22. When is synchronous request/response better than events?

## Part 4 — CQRS

23. What does CQRS separate?
24. Does CQRS require two databases?
25. Does CQRS require event sourcing?
26. What problem does a read projection solve?
27. What user-experience problem can projection lag create?
28. Give three signs that CQRS might be justified.
29. Give two signs that CRUD is still better.

## Part 5 — Event sourcing

30. What is the source of truth in event sourcing?
31. What is rehydration?
32. Why use snapshots?
33. Why do event-sourced systems often build projections?
34. How can stream versions prevent concurrent append conflicts?
35. Why is event schema evolution a major cost?
36. Difference between event sourcing and event-driven architecture?

## Part 6 — Sagas

37. What problem does a saga solve?
38. Difference between choreography and orchestration?
39. Why is compensation not the same as rollback?
40. Why must saga steps be idempotent?

---

# Scenario drills

## Scenario A — GPU workers

Your API is CPU-light, but transcription requires GPUs and queue-based autoscaling.

Answer:

- Do you need a microservice?
- Do you need an independently deployed worker application?
- What is the smallest architecture change that solves the problem?

## Scenario B — job completion consumers

After a job completes:

```text
billing
email
analytics
search
```

all need to react.

Would you use synchronous calls or events? Why?

## Scenario C — read-heavy job history

Job-history reads become 200× writes and require expensive joins.

Would you:

- add indexes,
- cache,
- create a projection,
- introduce full CQRS,
- extract a service?

Put them in the order you would investigate.

## Scenario D — billing audit

Enterprise customers require an immutable reconstruction of every usage credit, reservation, charge and reversal.

Compare:

- audit table,
- append-only ledger,
- event sourcing.

What extra requirement would justify full event sourcing?

## Scenario E — cancellation

Jobs, Billing and ML Processing have become independent services.

User cancels a running job.

Explain why a saga may now be necessary when it was unnecessary inside the original monolith.

---

# Architecture smell challenge

Explain what is suspicious about each sentence:

1. “We need microservices because we expect growth.”
2. “Every database table gets its own service.”
3. “CQRS means Kafka plus Elasticsearch.”
4. “We publish events, so we're event sourced.”
5. “The saga will roll back the GPU work.”
6. “We split the services, but all services query the same private tables.”
7. “We need event sourcing because audit logs are useful.”
8. “The read projection is eventually consistent, but billing balances must never be stale.”

---

# Final oral defense

Give yourself 3 minutes:

> Design the architecture of the transcription SaaS today, then describe the exact pressures that would justify introducing microservices, EDA, CQRS, event sourcing and a saga later.

A strong answer should contain at least **two patterns you explicitly reject for now**.
