# Week 5 Answer Key

Open only after attempting `review-and-quiz.md`.

These are concise reference answers. Your own answers should include examples and tradeoffs.

---

1. Long request lifetimes create timeout, resource-occupancy, deployment/retry and failure-isolation problems; job duration should not dictate API response lifetime.
2. It decouples producer/request timing from consumer/worker timing and provides buffering between rates.
3. A producer creates/publishes messages/work.
4. A consumer receives messages from the broker/log.
5. A worker is the application/process that performs the business computation, often acting as the consumer.
6. The request was accepted for processing but the final result is not ready.
7. Media belongs in object storage; large queue payloads amplify broker memory/disk/network/retry cost and hit size limits.
8. Depth counts waiting items; oldest age shows how long work has been waiting and is often closer to user pain.
9. Work may be lost, but is not intentionally redelivered.
10. Work should not be lost under the designed failure model, but redelivery/duplicates may occur.
11. Durable effect may commit while ACK is lost/crash occurs, causing redelivery.
12. Broker can remove/mark done before the durable business effect exists; crash then loses work.
13. At-least-once delivery plus idempotent/deduplicated business effects.
14. Exactly-once can apply only to a specified transactional system/state boundary; external side effects may remain outside it.
15. Publisher confirm says broker accepted publish responsibility; consumer ACK says consumer finished delivery responsibility.
16. It prevents consumers from being flooded with more unacknowledged/in-flight work than they can safely process.
17. Repeating it produces the same intended business effect as executing once.
18. A unique key atomically rejects a second record for the same logical operation/message.
19. They prevent duplicate/concurrent workers from moving state through invalid transitions.
20. `transcription:job_123:v1` or another stable logical operation ID.
21. Updating DB and broker as two independent writes creates a crash window where one succeeds and the other does not.
22. It records business state and publication intent atomically in one DB transaction.
23. Broker may receive publish while publisher loses confirmation before marking outbox sent; retry can duplicate.
24. To record processed message IDs/business effects transactionally and make duplicate consumption safe.
25. Marks a pending stream entry as successfully processed for a consumer group.
26. Tracks delivered-but-unacknowledged entries and their consumers.
27. Reassigning messages that have been pending/idle too long from failed/stuck consumers.
28. It receives publishes and routes them to queues via bindings/routing rules.
29. Isolating messages that are rejected, expired, exceed delivery policy, or otherwise cannot proceed normally.
30. A consumer/group's position in a partition/log.
31. Partitions; within one group a partition is actively owned by one consumer at a time.
32. Within a partition.
33. Transient failures may succeed later; permanent failures are unlikely to change without input/config/code change.
34. It reduces repeated pressure while a dependency recovers.
35. It prevents synchronized retry waves/thundering herds.
36. A message/work item that repeatedly fails due to its content/state.
37. Otherwise failed work silently accumulates with no diagnosis, retention, or safe recovery process.
38. Recovery traffic can overwhelm the just-recovered dependency and recreate the incident.
39. Examples: queue depth, oldest age, publish rate/failures, completion rate, processing p95/p99, pending/in-flight count, retry/redelivery rate, DLQ rate/age, consumer count.
40. Backlog grows without bound (until admission changes, capacity rises, traffic falls, or the system fails).

---

# Scenario guidance

## A — DB committed, broker offline

Outbox event remains durable. Publisher retries with bounded backoff until broker accepts. API/job history remains visible from PostgreSQL. Alert if outbox age grows.

## B — completed then crash before ACK

Message can redeliver. Idempotent worker sees job already completed / duplicate message and ACKs without redoing expensive/unsafe effects.

## C — provider 503 to every worker

Do not allow all workers to tight-loop. Backoff + jitter + provider concurrency/circuit/admission control; queue backlog becomes visible. Scale-down or pause can be safer than adding workers.

## D — corrupt video delivered 16 times

Failure classification/retry budget is broken. Mark permanent failure and/or dead-letter according to policy; stop spending capacity repeatedly.

## E — 8 Kafka partitions, 50 consumers

Within that consumer group, at most 8 consumers can actively own the 8 partitions at a time; the rest are idle regarding that topic assignment.

## F — RabbitMQ prefetch 100, 30-minute tasks

A consumer can hold huge amounts of work in-flight for hours, hurting fairness/recovery and hiding queue backlog. Use much smaller prefetch/concurrency aligned with real worker capacity.
