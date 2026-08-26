# Week 9 — Answer Key

Use only after attempting the review.

1. Replicas/derived state may temporarily diverge but converge after propagation if updates stop and the system is healthy.
2. Different facts have different freshness/correctness requirements and costs.
3. After a successful write, the same client observes that write on subsequent reads.
4. Once a client observes version N, later reads should not move backward to an older version.
5. Eventual/stale reads are allowed only within an explicit maximum/target lag.
6. Authority is a domain ownership decision; a derived copy may be newer/older without owning the fact.
7. Examples: cancellation authorization/state, billing ledger, job lifecycle transition.
8. Search index, analytics projection, dashboard aggregate.
9. During partition, maintaining stronger consistency may require refusing/defering work; maintaining availability may require accepting weaker/stale/divergent state.
10. Partition tolerance is generally required; C/A tradeoffs can differ per operation and topology.
11. Delay between authoritative commit and a replica applying that change.
12. Mutation commits on primary; immediate read hits replica before it applies the write.
13. Read primary temporarily; wait for replica/version; sticky/session routing; return mutation representation directly.
14. Users should not see progress move backward due to switching replicas.
15. Concurrent actors read same state and one silently overwrites the other's update.
16. Update only when stored version equals expected version, then increment version atomically.
17. The state/version no longer matched; another actor changed it or the transition is invalid.
18. MVCC is database snapshot/concurrency machinery; version column is explicit domain conflict detection.
19. Lost updates from stale state-changing HTTP requests.
20. High-contention short critical sections where blocking is preferable to repeated conflicts.
21. Two systems are updated separately and failure between them leaves durable disagreement.
22. Coordinator asks participants to prepare/promise commit capability.
23. Coordinator tells all prepared participants to commit, or roll back if prepare failed.
24. They can retain locks/resources and require coordinator/recovery decisions.
25. Those heterogeneous systems do not participate in the same local PostgreSQL transaction protocol.
26. Atomically records business state and intent-to-publish in one local DB transaction.
27. Command is intent/instruction; event is a fact that already occurred.
28. Work queue distributes one task among competing workers; pub/sub lets multiple independent consumers react.
29. Consumers update their own state asynchronously at different times.
30. Uncertain publication/ACK can produce duplicate deliveries.
31. Global ordering is expensive and often unnecessary; one entity/job only needs its own causal version order.
32. Durable dedup record keyed by consumer + event id, committed with local side effect.
33. Privacy exposure, huge payloads, duplication, schema coupling, retention complications.
34. Sequence of local transactions coordinated through continuation and compensation to reach a valid distributed outcome.
35. Choreography uses reactions to events; orchestration uses an explicit coordinator/workflow state machine.
36. It is a new business action that counteracts prior effects; it does not erase history/other concurrent changes.
37. Later comparison of durable systems/invariants to detect and repair divergence that ordinary retries did not resolve.
38. Message delivery state: published/pending/redelivered/acked according to broker semantics.
39. Redelivery can detect/reuse already-computed output rather than repeating expensive work.
40. Inspect DB; verify deterministic artifact and metadata; skip recomputation if valid; conditionally reconcile DB/progress; ACK only after state is safely accepted.
