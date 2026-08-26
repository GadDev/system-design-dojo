# Week 6 — Review & 40-Question Retrieval Quiz

## Rule

Answer without notes first. The discomfort is the learning signal.

---

# Part 1 — Fan-out / Fan-in

1. Define fan-out.
2. Define fan-in.
3. Why is fan-in a coordination problem rather than only a data-concatenation step?
4. How does the map/reduce mental model apply to transcription?
5. Difference between concurrency and parallelism?
6. Why can unlimited parallelism reduce reliability or throughput?
7. What is a straggler?
8. Why does the slowest required child affect parent latency?

# Part 2 — Partitioning

9. Why is chunk size a failure-domain decision?
10. Name three benefits of smaller chunks.
11. Name three costs of smaller chunks.
12. Fixed-duration vs silence-aware segmentation?
13. Why might overlapping chunks help transcription quality?
14. What new problem does overlap create?
15. Why should chunk identity include pipeline version?
16. What metrics would make you change chunk size?

# Part 3 — Orchestration

17. Why persist the fan-out plan?
18. Parent job vs child job?
19. What is a guarded state transition / compare-and-set?
20. Orchestration vs choreography?
21. Name four concurrency boundaries.
22. Why do per-tenant limits matter?
23. What makes cancellation tricky in a distributed workflow?
24. What durable state must survive an orchestrator restart?

# Part 4 — Aggregation

25. What is a fan-in barrier?
26. Why can a parent counter become incorrect?
27. Why reconcile child rows before merge?
28. Why must merge order use timestamps/index rather than completion order?
29. What makes a merge deterministic?
30. How can a guarded parent transition prevent two merges?
31. Strict vs partial completion policy?
32. Why can chunk-count progress give a misleading ETA?

# Part 5 — Race conditions & locks

33. Define race condition.
34. Give three races in the transcription pipeline.
35. Why are unique constraints often better than a distributed lock?
36. What is the stale-owner problem with leases?
37. What is a fencing token?
38. Why does a lock not remove the need for idempotency?
39. When could a PostgreSQL advisory lock be reasonable?
40. Give one trigger that would make you move from a custom DB+queue orchestrator to a durable workflow engine.

---

# Architecture reconstruction

Without notes, draw:

```text
Video
 ↓
Prepare
 ↓
Parent Job
 ↓
Chunk Plan
 ↓
Queue
 ├→ Worker
 ├→ Worker
 └→ Worker
 ↓
Chunk Results
 ↓
Barrier
 ↓
Merge
 ↓
Transcript
```

Add:

- PostgreSQL,
- object storage,
- retry/DLQ,
- concurrency limits,
- cancellation,
- idempotency boundary.

---

# Oral-defense prompts

Give yourself 2 minutes each:

### Prompt A

> Why retry one failed chunk instead of retrying a 90-minute video?

### Prompt B

> Why doesn't `completed_chunks == expected_chunks` by itself prove it is safe to merge?

### Prompt C

> Two workers both think they are the final chunk. Prevent duplicate merge without a Redis lock.

### Prompt D

> Why can a distributed lock expire while its owner is still executing, and why is that dangerous?

### Prompt E

> When would Temporal/Step Functions/Celery orchestration be justified over PostgreSQL + queue?

---

# Score

```text
36–40  excellent — move on
31–35  strong — review missed concepts
24–30  revisit Days 3–5
<24    rebuild the parent/child workflow from scratch
```

Do not optimize for the number. Optimize for explaining the **invariant** behind each answer.
