# Week 9 — 40-Question Review

Answer without notes first.

## Consistency models

1. What does eventual consistency promise at a high level?
2. Why should consistency be specified per operation/fact rather than per whole system?
3. Define read-your-writes.
4. Define monotonic reads.
5. What is bounded staleness?
6. Why is the newest copy not automatically the source of truth?
7. Give one transcription operation that should use authoritative state.
8. Give one derived view that can tolerate eventual consistency.

## CAP & replication

9. What tradeoff does CAP expose during a network partition?
10. Why is “pick any two” an oversimplification?
11. What is replica lag?
12. How can a read replica violate read-your-writes?
13. Give two ways to preserve read-after-write UX with lagging replicas.
14. Why might job progress need monotonic reads?

## Concurrency

15. What is a lost update?
16. How does a version column implement optimistic concurrency?
17. What does zero affected rows mean in a compare-and-swap update?
18. Application version column vs MVCC?
19. What does HTTP `If-Match` protect against?
20. When might pessimistic row locking be preferable?

## Distributed transactions

21. What is the dual-write problem?
22. What happens in phase 1 of 2PC?
23. What happens in phase 2?
24. Why can prepared transactions be dangerous if left open?
25. Why can't a normal PostgreSQL transaction atomically include arbitrary R2 and AI-provider calls?
26. What does a transactional outbox solve?

## Event-driven architecture

27. Command vs event?
28. Work queue vs publish-subscribe?
29. Why does EDA often create eventual consistency?
30. Why does outbox publication still require idempotent consumers?
31. Why is per-aggregate event ordering often sufficient?
32. What is an inbox/processed-event table?
33. Give one risk of putting full transcript text into events.

## Saga & reconciliation

34. What is a saga?
35. Choreography vs orchestration?
36. Why is compensation not a rollback?
37. What is reconciliation?
38. In the transcription design, what should the queue be authoritative for?
39. Why do deterministic artifact keys help recovery?
40. Worker wrote R2 result but DB update failed: what should happen on redelivery?

---

## Score

| Score | Meaning |
|---|---|
| 36–40 | Strong — you can reason about distributed state disagreements |
| 31–35 | Good — revisit one weak consistency/concurrency area |
| 24–30 | Re-run optimistic-locking + reconciliation labs |
| <24 | Rebuild source-of-truth and failure-window mental models |
