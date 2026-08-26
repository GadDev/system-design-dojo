# Week 6 — Answer Key

Use only after attempting the review.

## Short answers

1. Split one logical workload into multiple independently executable child tasks.
2. Coordinate/join child results into a parent result after a defined barrier.
3. Completion order, duplicates, failures, durable output and competing finalizers must be coordinated.
4. Chunk transcription is map-like; transcript merge is reduce-like.
5. Concurrency = overlapping progress; parallelism = simultaneous execution on separate capacity.
6. Dependencies, provider quotas, DB/storage/network capacity and coordination overhead become bottlenecks.
7. A child whose latency is unusually high compared with peers.
8. Fan-in usually waits for every required child, so tail child latency becomes parent latency.
9. It defines what gets scheduled/retried/timed out/cancelled as a unit.
10. Fine retry granularity, better load balance, finer progress, more scheduling flexibility.
11. More tasks/messages/metadata, more merge boundaries, more scheduling overhead.
12. Fixed is predictable; silence-aware may improve linguistic boundaries but creates uneven task sizes.
13. It preserves context around boundaries.
14. Duplicate words/timestamps must be reconciled.
15. Reprocessing with a changed model/prompt/pipeline must not collide with old results.
16. p95 task time, retries, scheduling overhead, context/merge quality, provider efficiency, straggler ratio.
17. So restart/recovery does not depend on volatile process memory and duplicate creation can be detected.
18. Parent = logical media workflow; child = one independently schedulable partition.
19. Update occurs only if current state/version matches expected state/version.
20. Orchestration uses an explicit coordinator; choreography reacts through distributed events.
21. Global, provider, tenant, parent-job, GPU/CPU pool are examples.
22. Prevents one tenant from monopolizing all capacity.
23. Running work, queued work and finalization may all race with the cancellation intent.
24. Child plan/status, parent state, desired state/cancellation, retries, merge state, versions.
25. Business condition required before aggregate/finalizer is allowed.
26. Duplicate completion or crashes between updates can cause drift.
27. A counter is an optimization; durable child rows/artifacts are closer to authoritative evidence.
28. Completion order is nondeterministic.
29. Same input set + same version/rules produces same logical output.
30. Atomic conditional update from PROCESSING → MERGING lets only one logical caller claim it.
31. Strict requires all required children; partial permits an explicitly incomplete result.
32. Child costs vary; 90% of count may not mean 90% of wall-clock work.
33. Correctness depends on interleaving/timing of concurrent operations.
34. Duplicate child execution, duplicate merge, cancel/complete, retry/original, counter increment races.
35. They enforce the invariant atomically at the source of truth without lease/ownership failure modes.
36. Owner may pause longer than TTL and continue acting after another owner acquires the lock.
37. Increasing token used by downstream resource to reject stale owners.
38. Ambiguous network failures can still cause an operation to be retried after effects happened.
39. When contenders all coordinate through one PostgreSQL primary and exclusive application-defined work is short-lived.
40. Long-lived/multi-stage workflows, dynamic fan-out, complex cancellation/timers, repeated coordination bugs, poor visibility.

---

## What a strong Week 6 design contains

```text
explicit parent/child identities
bounded concurrency
idempotent child effects
persistent workflow state
deterministic chunk ordering
a clear barrier policy
duplicate-safe finalization
race handling without unnecessary locks
retries scoped to the child failure domain
metrics for tail latency and retry amplification
```
