# Week 3 — Caching Cheat Sheet

## Core path

```text
Client
  ↓
API
  ↓
Redis
 ├─ HIT  → return
 └─ MISS → PostgreSQL → cache → return
```

---

# Cache

A temporary/derived copy used to reduce latency or load.

Typical principle:

```text
cache loss → performance problem
not data-loss problem
```

---

# Cache-aside

Read:

```text
GET cache
↓ MISS
GET database
↓
SET cache + TTL
↓
return
```

Write:

```text
UPDATE database
↓
DELETE cache key
```

---

# Hit ratio

```text
hits / (hits + misses)
```

Origin QPS approximation:

```text
request QPS × miss ratio
```

---

# TTL

```text
time to live
```

Use staleness requirement to choose it.

```text
short TTL
→ fresher
→ more misses

long TTL
→ more hits
→ more stale risk
```

---

# Expiration vs eviction

```text
Expiration = key lifetime/freshness
Eviction   = memory pressure/capacity
```

A non-expired key may still be evicted.

---

# Invalidation

Common:

```text
write DB
↓
DEL cache
```

TTL often acts as a safety net.

---

# Negative caching

```text
missing key → cache NOT_FOUND briefly
```

Useful against repeated misses.

Risk:

```text
stale not-found
memory abuse
```

---

# Cache penetration

Repeated requests for uncached/nonexistent data reach the origin.

---

# Cache stampede

```text
popular key expires
↓
many simultaneous misses
↓
origin flood
```

Mitigations:

```text
request coalescing
TTL jitter
early refresh
stale-while-revalidate
edge caching
```

---

# Hot key

One key receives disproportionate traffic.

```text
many shards ≠ one hot key split across shards
```

Mitigations:

```text
CDN
L1 local cache
logical key replication
more capacity
```

---

# Cache pollution

One-off/cold values push useful hot data out of cache.

---

# Redis memory policies

Know the idea:

```text
LRU → recently used
LFU → frequently used
```

Redis supports multiple eviction policies.

Do not memorize every one.

---

# Distributed cache

```text
API 1 ─┐
API 2 ─┼→ Redis
API 3 ─┘
```

Benefits:

```text
shared working set
central invalidation
```

Costs:

```text
network dependency
shared failure
ops complexity
```

---

# Redis Cluster

```text
key
↓
hash
↓
one of 16,384 slots
↓
cluster node
```

Hash tags:

```text
{user:42}:profile
{user:42}:settings
```

can force related keys into one slot.

---

# Multi-level cache

```text
L1 local memory
↓ MISS
L2 Redis
↓ MISS
PostgreSQL
```

Faster.

More invalidation complexity.

---

# Cache failure

Possible strategies:

```text
fail open → DB
fail closed → error
serve stale
shed load
```

Never choose without considering origin capacity.

---

# Essential metrics

```text
hit ratio
misses/sec
cache p50/p95/p99
Redis errors/timeouts
memory
evictions
expired keys
hot keys
per-shard CPU
DB QPS
DB latency
fallback rate
```

---

# URL shortener

Key:

```text
url:v1:{short_code}
```

DB query:

```sql
WHERE short_code = ?
```

TTL:

```text
min(cache TTL, remaining URL lifetime)
```

Popular URL:

```text
consider CDN before clever Redis tricks
```

---

# Questions to ask every time

```text
What is the source of truth?
Why cache this?
What is the key?
How stale may it be?
How is it invalidated?
What if Redis disappears?
What metric proves value?
```
