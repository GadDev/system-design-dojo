# Day 1 — Cache Fundamentals & Redis: Faster by Copying Data

## Goal

Understand what a cache changes in a system, why Redis is useful, and which workloads are actually cache-shaped.

## Timebox

- 15 min — cache mental model
- 20 min — Redis as a cache
- 15 min — latency / hit-ratio reasoning
- 15 min — local Redis lab
- 10 min — retrieval quiz

---

# 1. A cache is a copy

Suppose PostgreSQL is authoritative:

```text
PostgreSQL
user 42 → {"name":"Ada"}
```

Redis may hold:

```text
user:42 → {"name":"Ada"}
```

That Redis value is not automatically truth.

It is a **derived copy**.

This gives us the most important caching invariant of the week:

> Losing cache data should usually hurt performance—not correctness.

If deleting your cache loses business data, you are not using it merely as a cache anymore.

---

# 2. Why caching helps

Imagine:

```text
PostgreSQL lookup p95 = 25 ms
Redis lookup p95      = 1 ms
```

If the same record is requested repeatedly, Redis can:

- reduce application latency,
- reduce database query volume,
- reduce database connection pressure,
- absorb traffic spikes,
- reduce repeated expensive computation.

But every cache lookup also adds:

- another dependency,
- another network hop,
- memory cost,
- stale-data risk,
- operational complexity.

Caching is therefore not:

```text
Redis = faster
```

It is:

```text
latency ↓
origin load ↓
memory cost ↑
consistency complexity ↑
failure modes ↑
```

---

# 3. Cache-shaped workloads

Caching tends to work well when:

- reads repeat,
- reads greatly outnumber writes,
- the origin is significantly slower,
- the data can tolerate some staleness,
- the working set is smaller than the total dataset,
- the value is expensive to compute or retrieve.

Examples:

```text
popular public profiles
product catalog entries
feature configuration
URL redirect targets
expensive report fragments
```

Caching may help less when:

- every request reads a different object,
- data changes constantly,
- stale data is unacceptable,
- values are very large,
- the cache lookup costs nearly as much as the origin read.

---

# 4. Redis mental model

Redis is an in-memory data system that exposes key-based operations.

For a simple cache:

```text
key                  value
------------------------------------------------
profile:42           JSON profile
url:abC91            https://example.com/article
job:123:summary      compact job metadata
```

A simple lookup:

```bash
SET profile:42 '{"name":"Ada"}'
GET profile:42
```

Add expiration:

```bash
SET profile:42 '{"name":"Ada"}' EX 300
```

Now the value expires after roughly five minutes.

---

# 5. Redis is fast, but network still exists

Redis is memory-oriented, but a distributed cache is still a network service.

The path is:

```text
API
 ↓ TCP/network
Redis
 ↓
API
```

So end-to-end latency includes:

```text
client serialization
network RTT
Redis command execution
response deserialization
```

Do not confuse "in memory" with "zero latency."

At high request volume, avoiding unnecessary round trips can matter.

---

# 6. The cache hit ratio

Define:

```text
hit ratio = cache hits / total cache lookups
```

Example:

```text
9,000 hits
1,000 misses
-----------
10,000 lookups

hit ratio = 90%
```

If a cache miss still hits PostgreSQL, then database reads become approximately:

```text
total reads × miss ratio
```

With:

```text
20,000 reads/sec
95% hit ratio
```

origin load is roughly:

```text
20,000 × 0.05 = 1,000 reads/sec
```

That is why hit ratio is not vanity telemetry.

It directly changes origin pressure.

---

# 7. But hit ratio alone can lie

Imagine two systems:

### System A

```text
99% hit ratio
cache p99 = 80 ms
```

### System B

```text
90% hit ratio
cache p99 = 2 ms
database easily handles misses
```

System A is not automatically better.

Measure:

- hit rate,
- cache latency,
- origin latency,
- origin QPS,
- memory usage,
- eviction rate,
- error rate.

---

# 8. Local cache vs distributed cache

## Local in-process cache

```text
API-1 memory
```

Benefits:

- extremely low latency,
- no network hop.

Problems:

- each API has its own copy,
- invalidation becomes instance-specific,
- memory duplicates across instances,
- values diverge.

## Distributed cache

```text
API-1 ─┐
API-2 ─┼→ Redis
API-3 ─┘
```

Benefits:

- shared working set,
- centralized invalidation,
- independent application instances.

Costs:

- network dependency,
- shared failure domain,
- operational complexity.

You will revisit this on Day 5.

---

# 9. Apply it to the transcription platform

Consider these candidates:

| Data | Cache candidate? | Why / why not? |
|---|---|---|
| User's job history | ? | |
| Job progress | ? | |
| Completed transcript | ? | |
| Pricing configuration | ? | |
| Uploaded raw video | ? | |
| Presigned upload URL | ? | |

Do not answer based on object size alone.

Ask:

```text
How often read?
How often changed?
How expensive origin read?
How stale can it be?
Is it sensitive?
```

---

# Lab — run Redis

Use [`labs/local-redis.md`](./labs/local-redis.md).

Try:

```bash
SET hello world
GET hello

SET ephemeral value EX 10
TTL ephemeral

DEL hello
GET hello
```

Then inspect:

```bash
INFO memory
INFO stats
```

Do not memorize the output.

Find:

- used memory,
- keyspace hits,
- keyspace misses.

---

# Exercise — cache suitability matrix

Complete:

| Resource | Read frequency | Write frequency | Staleness tolerance | Expensive origin? | Cache? |
|---|---:|---:|---|---|---|
| Public URL redirect | high | low | seconds/minutes | moderate | ? |
| Bank balance | medium | high | near-zero | moderate | ? |
| Pricing configuration | high | low | minutes | low | ? |
| Job progress | high while active | frequent | seconds | low | ? |
| Static country list | high | rare | hours | low | ? |

For every `yes`, justify:

```text
value
key
TTL
source of truth
failure behavior
```

---

# Break it 💥

Predict the result when:

1. Redis is 100% unavailable.
2. Redis latency jumps from 1 ms to 300 ms.
3. The cache contains a stale profile.
4. Your hit ratio falls from 95% to 20%.
5. API instances each maintain independent in-memory caches.

For each:

```text
user symptom
origin impact
metric that reveals it
```

---

# Retrieval quiz

1. Why is a cache normally not the source of truth?
2. What is cache hit ratio?
3. Why can a high hit ratio still coexist with poor performance?
4. Give three properties of a cache-shaped workload.
5. Why is an in-process cache harder to invalidate across API replicas?
6. What new dependency does a distributed cache introduce?
7. What should usually happen if all cache data disappears?

## Exit criterion

You can explain caching as a **latency/load/freshness tradeoff**, not as "put Redis in front of PostgreSQL."
