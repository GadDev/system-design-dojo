# Week 7 — Review & 40-Question Retrieval Quiz

## Rule

Answer without notes first.

---

# Part 1 — Failure & Timeouts

1. Why is “slow” a failure mode even when responses eventually return `200`?
2. Timeout vs deadline?
3. Connection timeout vs request/read timeout?
4. Why can a timeout be too short?
5. Why can a timeout be too long?
6. Why does a timeout not prove the remote side effect did not happen?
7. What should inform a timeout value?
8. Why should retries fit inside an overall deadline/retry budget?

# Part 2 — Retries

9. Give three retryable failure examples.
10. Give three failures you usually should not blindly retry.
11. Why can retries cause cascading failure?
12. Define exponential backoff.
13. Why cap exponential backoff?
14. What problem does jitter solve?
15. Why are nested retries dangerous?
16. Why must a mutating retry be idempotent?

# Part 3 — Circuit Breakers & Bulkheads

17. Describe CLOSED state.
18. Describe OPEN state.
19. Describe HALF_OPEN state.
20. Why is minimum sample size useful?
21. Why can slow-call rate trip a breaker?
22. Circuit breaker vs timeout?
23. Circuit breaker vs rate limiter?
24. What is a bulkhead?

# Part 4 — Degradation & Health

25. Define graceful degradation.
26. Hard dependency vs soft dependency?
27. What does startup probe answer?
28. What does liveness probe answer?
29. What does readiness probe answer?
30. Why can checking PostgreSQL in liveness be dangerous?
31. Why mark an API unready before terminating it?
32. Give one safe degraded mode for the transcription product.

# Part 5 — Failover & Recovery

33. Define RTO.
34. Define RPO.
35. Why can asynchronous replication have non-zero RPO?
36. What is split brain?
37. Why is failback/rebuilding redundancy part of the incident?
38. Why can AI-provider fallback change business semantics?
39. How should a worker recover if output was written but ACK/state commit was lost?
40. What evidence would convince you a dependency is safe to receive full traffic again?

---

# Architecture reconstruction

Without notes, draw the transcription system and annotate every remote boundary with:

```text
timeout
retry
idempotency
breaker/bulkhead
degraded mode
```

Then mark stateful dependencies with:

```text
RTO
RPO
failover
```

---

# Oral-defense prompts

### Prompt A

> AI provider returns 429 for ten minutes. Why might adding workers make the outage worse?

### Prompt B

> Redis cache goes down. Why can a “fallback to PostgreSQL” design still take down the system?

### Prompt C

> PostgreSQL is slow, not dead. What mechanisms stop the slowness from consuming every API and worker resource?

### Prompt D

> Worker dies after writing chunk output but before ACK. Show duplicate-safe recovery.

### Prompt E

> Explain why failover, RPO and split brain belong in the same conversation.

---

# Score

```text
36–40  excellent — move to observability
31–35  strong — review missed categories
24–30  revisit Days 2–5
<24    rebuild the reliability matrix
```
