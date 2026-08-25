# Week 3 — Review & Retrieval Quiz

## Goal

Prove that you can reason about a cache without reaching for notes or saying "Redis is fast."

## Timebox

- 15 min — blank-page architecture
- 30 min — 40-question quiz
- 20 min — incident scenarios
- 20 min — oral explanations
- 15 min — correction log

---

# Part 1 — Blank-page challenge

Draw from memory:

```text
Client
 ↓
API
 ↓
Redis
 ↓ MISS
PostgreSQL
```

Annotate:

- cache hit,
- cache miss,
- fill,
- TTL,
- invalidation,
- Redis failure,
- DB fallback.

Then add:

```text
CDN / edge
```

and explain when it can reduce Redis pressure.

---

# Part 2 — 40 questions

## Fundamentals

1. What is the source of truth in ordinary cache-aside?
2. Why can a cache reduce database connection pressure?
3. Define cache hit.
4. Define cache miss.
5. Define hit ratio.
6. Why is a high hit ratio not sufficient to prove good performance?
7. What is a cache-shaped workload?
8. Why can a cache miss be slower than a no-cache read?

## Cache-aside

9. List the read steps of cache-aside.
10. Who is responsible for cache-aside logic?
11. What happens after a miss retrieves data from PostgreSQL?
12. Why can key versioning be useful?
13. Why is `42` a poor cache key?
14. Why is whole-object caching often simpler than field-level caching?
15. What is negative caching?
16. What is cache penetration?

## TTL / invalidation / eviction

17. What business question should determine TTL?
18. Difference between expiration and eviction?
19. Can Redis evict a non-expired key?
20. Why combine explicit invalidation with TTL?
21. What is TTL jitter?
22. Why might identical TTLs trigger a traffic spike?
23. Explain LRU at a high level.
24. Explain LFU at a high level.
25. Why must a cache TTL not outlive a domain-level URL expiry?
26. Why is TTL-only invalidation sometimes insufficient?

## Failure patterns

27. What is a cache stampede?
28. Why can Redis failure cascade into PostgreSQL failure?
29. What is request coalescing?
30. What does stale-while-revalidate trade?
31. What is a hot key?
32. Why does sharding not automatically solve a hot key?
33. What is cache pollution?
34. Why can negative caching itself be abused?

## Distributed cache

35. Difference between local and distributed cache?
36. What is a Redis Cluster hash slot?
37. Why do cluster-aware clients matter?
38. What are Redis hash tags?
39. What new complexity does L1 + L2 caching introduce?
40. What metrics tell you whether caching is helping?

---

# Part 3 — Incident scenarios

## Incident A — cache latency

```text
hit rate = 99%
Redis p99 = 900 ms
DB p99 = 40 ms
```

Questions:

1. Why is the endpoint slow?
2. Is hit ratio useful here?
3. What timeout/bypass strategy would you investigate?
4. Which Redis diagnostics would you inspect?

---

## Incident B — cache outage

```text
Redis unavailable
↓
API falls back to DB
↓
DB connections saturate
```

Questions:

1. What coupling caused the cascade?
2. How could admission control help?
3. What does "origin headroom" mean?
4. How could CDN caching change the URL-shortener failure path?

---

## Incident C — stale deletion

```text
Link deleted in PostgreSQL
Redis DEL failed
TTL = 1 hour
```

Questions:

1. What correctness bug exists?
2. Is one-hour stale behavior acceptable?
3. What does TTL bound?
4. What stronger invalidation mechanism might you consider?

---

## Incident D — celebrity URL

```text
one URL = 45% of traffic
Redis Cluster has 12 shards
one shard = 100% CPU
others = 20%
```

Questions:

1. Why didn't clustering solve the problem?
2. Which metric would expose the skew?
3. Could the CDN absorb it?
4. Could L1 caching help?
5. What tradeoff do those mitigations add?

---

# Part 4 — explain aloud

Give yourself 90 seconds each:

### Prompt A

> Explain cache-aside to a backend engineer.

### Prompt B

> Why is cache invalidation difficult?

### Prompt C

> Explain expiration vs eviction.

### Prompt D

> Redis is down. What should the API do?

### Prompt E

> Why doesn't Redis Cluster automatically solve hot keys?

### Prompt F

> Why might a URL shortener benefit more from caching than a transcription job-status endpoint?

If you name a technology, connect it to a requirement.

---

# Part 5 — self-score

| Score | Meaning |
|---|---|
| 36–40 | Strong — proceed |
| 31–35 | Good — review 1–2 weak areas |
| 24–30 | Revisit Days 2–5 |
| <24 | Rebuild cache-aside and failure model |

---

# Final deliverable

Create:

```text
my-cache-design.md
```

Answer:

> Where would I add caching to my transcription platform today, where would I explicitly not add it, and what measurements would cause me to change that decision?

That is a much better portfolio artifact than:

> "We use Redis because it scales."
