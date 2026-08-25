# Week 3 — Answer Key

Use this **after** attempting the exercises.

These are model answers, not universal truths.

---

# Day 1 — cache suitability examples

## Public URL redirect

Likely cacheable.

Why:

```text
read-heavy
small value
stable
latency sensitive
```

## Bank balance

Do not casually apply ordinary stale cache-aside semantics.

Correctness/read-after-write requirements dominate.

## Pricing configuration

Often a good cache candidate:

```text
small
frequently read
rarely changed
```

## Job progress

Maybe.

At modest scale PostgreSQL polling may be simpler.

At large polling volume, Redis or push-oriented progress architecture may help.

## Static country list

Excellent local/distributed cache candidate; may even be bundled/versioned with the app.

---

# Day 2 — cache-aside

Read miss:

```text
Redis GET
MISS
PostgreSQL SELECT
Redis SET + TTL
return
```

Write:

```text
PostgreSQL commit
Redis DEL
```

Why DB first?

Because the DB remains authoritative.

If Redis deletion fails, TTL limits stale duration.

---

# Negative caching

Useful for:

```text
repeated nonexistent URL codes
```

Use short TTL.

Avoid unbounded attacker-generated negative entries.

---

# Day 3 — TTL

Good answer shape:

```text
staleness requirement
↓
TTL
```

rather than:

```text
standard 5 minutes
```

Expiration and eviction differ:

```text
expiration = time
eviction = memory pressure
```

---

# Day 4 — outage cascade

If:

```text
100k req/s
98% hit
```

DB receives about:

```text
2k req/s
```

If cache disappears and every request falls back:

```text
~100k req/s
```

Origin overload is predictable unless protected.

Mitigations can include:

- circuit breaker,
- fallback concurrency cap,
- rate limiting/load shedding,
- CDN,
- origin capacity/headroom,
- serving stale where valid.

---

# Hot key

Clustering does not automatically split one key.

Mitigation may happen above Redis:

```text
CDN
local L1
```

This is often better than application-level key replication.

---

# Day 5 — Redis Cluster

Redis Cluster uses:

```text
16,384 hash slots
```

Keys map to slots, slots map to cluster nodes.

Hash tags deliberately colocate keys.

Use only when the multi-key access pattern needs it.

---

# Day 6 — transcription cache

A defensible current-stage design might be:

```text
Do not cache most job state yet.
```

Why:

- PostgreSQL indexed lookup is cheap,
- job volume may not justify another dependency,
- progress changes frequently,
- correctness/debugging is simpler.

Potential early cache candidate:

```text
pricing/configuration
```

Potential later candidate:

```text
high-volume job summaries
```

after metrics show DB/query pressure.

Large final transcripts are usually not ideal RAM-cache candidates unless there is a proven repeated-read workload.

---

# Day 7 — URL shortener

Strong baseline:

```text
Client
↓
CDN/edge where safe
↓
LB
↓
stateless API
↓
Redis cache-aside
↓ MISS
PostgreSQL
```

PostgreSQL:

```text
UNIQUE(short_code)
```

Cache:

```text
url:v1:{short_code}
```

TTL:

```text
min(normal TTL, remaining domain lifetime)
```

Delete:

```text
DB authoritative delete/soft-delete
↓
cache invalidation
```

Unknown codes:

```text
short negative cache
```

Hot link:

```text
prefer edge/CDN offload when semantics permit
```

Redis outage:

```text
controlled fallback
not unlimited DB flood
```

Metrics:

```text
redirect p99
edge hit ratio
Redis hit ratio
Redis latency
DB lookup QPS
DB latency
fallback rate
evictions
hot keys
```

---

# 301 vs 302/307

A permanent redirect may be cached aggressively by clients/edges, reducing backend traffic but reducing control and potentially bypassing analytics.

A temporary redirect retains more control but costs more request traffic.

There is no universally correct choice.

The requirement decides.
