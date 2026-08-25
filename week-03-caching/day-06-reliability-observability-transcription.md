# Day 6 — Cache Reliability, Observability & the Transcription Platform

## Goal

Decide whether a cache is helping in production and design graceful behavior when it is slow, stale, cold, or unavailable.

## Timebox

- 20 min — reliability model
- 20 min — cache metrics
- 20 min — graceful degradation
- 25 min — transcription cache review
- 15 min — design write-up
- 10 min — retrieval quiz

---

# 1. Redis is now a dependency

Before:

```text
API → PostgreSQL
```

After:

```text
API → Redis → maybe PostgreSQL
```

You improved the happy path.

You also added:

```text
Redis timeout
Redis connection exhaustion
Redis CPU saturation
network failure
evictions
cold-cache events
stale values
```

This is the recurring system-design pattern:

> Every performance optimization changes the failure graph.

---

# 2. Choose cache failure behavior

If Redis times out, options include:

## Fail open to origin

```text
Redis error
↓
PostgreSQL
```

Good for availability.

Danger:

```text
Redis outage
↓
mass fallback
↓
DB overload
```

## Fail closed

Return an error instead of hitting origin.

Protects DB.

Hurts availability.

## Serve stale

If an older value exists somewhere and product semantics allow.

Protects latency/origin.

Trades freshness.

## Shed load

Reject/defer some requests.

Protects the system at the expense of some clients.

No universal answer.

---

# 3. Timeouts matter

Do not allow:

```text
Redis timeout = 5 seconds
```

when:

```text
endpoint SLO = 300 ms
```

Dependency timeouts should fit inside the end-to-end latency budget.

Example mental model:

```text
endpoint p99 target = 250 ms

Redis budget = 20 ms
DB fallback budget = 150 ms
serialization/network/etc = remainder
```

Numbers depend on the service.

The principle does not.

---

# 4. Metrics that matter

## Cache performance

```text
hit ratio
miss ratio
GET/SET latency
p50/p95/p99 latency
```

## Capacity

```text
used memory
memory fragmentation
evictions/sec
expired keys/sec
key count
```

## Reliability

```text
Redis errors
timeouts
connection failures
failovers
```

## Origin protection

```text
PostgreSQL QPS
DB connection-pool usage
DB latency
fallback rate
```

## Skew

```text
per-shard CPU
per-shard memory
hot keys
top key traffic share
```

A cache dashboard that shows only "Redis CPU" is not enough.

---

# 5. The cache hit ratio formula

```text
hit ratio =
hits / (hits + misses)
```

But segment it.

Overall:

```text
95%
```

might hide:

```text
URL redirects     99.8%
job progress      15%
profiles          80%
```

Different workloads need different decisions.

---

# 6. Cost-per-hit thinking

Suppose Redis costs:

```text
€500/month
```

and removes:

```text
90% of 20k DB reads/sec
```

Great.

But if it removes:

```text
3 DB reads/sec
```

you may be paying for architecture cosplay.

Caching should have measurable value.

---

# 7. Cold-cache event

Examples:

- Redis restart,
- flush,
- new cluster,
- deployment with new key namespace,
- large eviction event.

Cold cache:

```text
hit ratio → near zero
origin load → spike
latency → spike
```

Mitigations:

- origin headroom,
- gradual traffic ramp,
- selective prewarming,
- staggered namespace changes,
- request coalescing,
- rate limiting.

---

# 8. Prewarming

You may preload:

```text
top 1,000 popular URLs
```

before opening traffic.

This can help predictable hot sets.

But prewarming everything:

```text
database → copy entire dataset → Redis
```

can:

- delay startup,
- waste memory,
- overwhelm DB,
- cache cold data.

Cache-aside exists partly because the working set is often smaller than the dataset.

---

# 9. Transcription platform cache review

Now evaluate your own application.

## Candidate A — job progress

Pattern:

```text
GET /jobs/{id}
```

Properties:

```text
read frequently while processing
changes frequently
small value
staleness tolerance maybe 1–5 sec
private
DB read is probably cheap
```

Question:

> Is Redis useful, or would polling PostgreSQL at your current scale be simpler?

A senior design is allowed to answer:

```text
Not yet.
```

---

# 10. Candidate B — completed transcript

Properties:

```text
large
immutable-ish after completion
read less frequently
possibly sensitive
```

Possible architectures:

### DB/R2 only

Simple.

### Redis cache

Potentially expensive in RAM for large text.

### CDN/object storage

Potentially better for export/download depending on access/auth requirements.

Caching is not automatically "Redis."

---

# 11. Candidate C — plan/pricing/config

Properties:

```text
small
read frequently
changes rarely
same across many requests
```

Excellent cache shape.

Could even be:

```text
short local L1
+
distributed configuration/cache
```

depending on requirements.

---

# 12. Candidate D — signed upload URL

Presigned URLs already have:

```text
expiration
authorization implications
```

Caching and reusing them carelessly may expand their lifetime or share scope incorrectly.

Security semantics beat cache hit ratio.

---

# 13. Candidate E — user profile

Likely:

```text
small
read repeatedly
moderate staleness tolerance
```

Could be cacheable.

But first measure whether PostgreSQL actually needs help.

---

# 14. Cache decision record

Use:

[`cache-decision-template.md`](./cache-decision-template.md)

Complete one ADR-style record for:

```text
GET /jobs/{id}
```

Your answer may be:

```text
Do not add Redis at current scale.
```

That can be the better system-design decision.

---

# Exercise — architecture review

Given:

```mermaid
flowchart LR
    Browser --> API
    API --> Redis[(Redis)]
    Redis --> DB[(PostgreSQL)]
```

Answer:

1. What if Redis is optional rather than authoritative?
2. What timeout should API use?
3. What happens when Redis is slow but not completely down?
4. How do we prevent fallback from crushing PostgreSQL?
5. Which metrics detect cache value?
6. What staleness is permitted?
7. Who invalidates?
8. What gets cached?
9. What must never be cached?
10. What is the cold-start plan?

---

# Break it 💥

At 10:00:

```text
Redis p95 1 ms
hit rate 97%
DB CPU 25%
```

At 10:10:

```text
Redis p95 450 ms
hit rate 97%
DB CPU 25%
API p95 600 ms
```

Nothing is "missing."

Why is the product slow?

This is the lesson:

> A cache HIT can still be a slow dependency call.

Now another incident:

```text
Redis completely fails
API skips cache
DB CPU 100%
```

Which failure mode is worse?

It depends on your fallback and protection design.

---

# Retrieval quiz

1. What new failure categories appear when Redis is added?
2. What does "fail open to origin" mean?
3. Why can fail-open cause cascading failure?
4. Why must dependency timeout fit the endpoint latency budget?
5. List five cache metrics.
6. Why segment hit ratio by workload?
7. What is a cold-cache event?
8. When is prewarming useful?
9. Why might Redis be a poor place for large transcripts?
10. Why can "do not cache yet" be a senior decision?
11. What should cache failure normally affect if PostgreSQL is authoritative?
12. Why is a 97% hit ratio not proof that the cache is healthy?

## Exit criterion

You can review a cache as a **production dependency**, including latency, failure, origin protection, and cost.
