# Week 3 — Sources, Books & Reading Map

This is the curated bibliography for Week 3.

**Reference cache:** Redis.

**Reference source of truth:** PostgreSQL.

**Verified for this course revision:** August 2026.

Source priority:

1. Redis official documentation,
2. architecture-pattern documentation,
3. durable system-design books,
4. production case studies,
5. interview material.

---

# Day 1 — Redis / cache fundamentals

## Redis — cache-aside use case

https://redis.io/docs/latest/develop/use-cases/cache-aside/

Read for:

- repeated read workloads,
- cache-aside,
- TTL-bounded staleness,
- stampede motivation,
- shared cache vs local cache.

Key lesson:

Redis is most useful when a working set is read repeatedly and the primary database should not pay full read cost every time.

## Redis — Optimization

https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/

Use as an entry point for:

- latency,
- benchmarking,
- memory optimization.

## Redis — Diagnosing latency

https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/

Read selectively.

Important system-design ideas:

- Redis itself may execute quickly while network/system latency still matters.
- round trips matter,
- slow commands matter,
- production latency requires measurement.

---

# Day 2 — cache-aside

## Microsoft Azure Architecture Center — Cache-Aside pattern

https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside

Vendor-specific examples, but the architectural pattern is broadly applicable.

Focus on:

- read miss flow,
- update + invalidation,
- lifetime,
- consistency,
- local vs shared cache,
- when cache-aside is a bad fit.

## Redis — cache-aside

https://redis.io/docs/latest/develop/use-cases/cache-aside/

Re-read with implementation eyes.

Focus on:

```text
GET
SET with TTL
DEL on update
```

and the fact that the application owns consistency.

---

# Day 3 — TTL, expiration & eviction

## Redis — TTL

https://redis.io/docs/latest/commands/ttl/

Read for:

- remaining TTL,
- special return values,
- introspection.

## Redis — EXPIRE

https://redis.io/docs/latest/commands/expire/

Read for:

- expiration behavior,
- conditional expiry options.

## Redis — Key eviction

https://redis.io/docs/latest/develop/reference/eviction/

Required.

Focus on:

- `maxmemory`,
- eviction policy,
- LRU/LFU intuition,
- `noeviction`,
- why expiration and eviction are different.

Do not memorize every policy.

Understand what problem each class of policy solves.

---

# Day 4 — hot keys / stampedes

## Redis — Hot-key observability

https://redis.io/docs/latest/operate/rs/monitoring/observability/

Focus on the Hot Keys section.

Key lesson:

A single frequently accessed key can saturate one shard because a key belongs to one shard.

## Redis — HOTKEYS command

https://redis.io/docs/latest/commands/hotkeys/

Redis Open Source 8.6 introduces dedicated hot-key tracking commands.

Treat this as operational tooling, not as the definition of the architecture problem.

## Redis — cache-aside production guidance

https://redis.io/docs/latest/develop/use-cases/cache-aside/

Read the sections discussing stampede mitigation and TTL-bounded staleness.

---

# Day 5 — distributed cache / Redis Cluster

## Redis Cluster Specification

https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/

Required concepts:

- Redis Cluster goals,
- 16,384 hash slots,
- key-to-slot mapping,
- hash tags,
- slot movement / resharding,
- failover model.

Do **not** read the whole specification in one sitting unless you enjoy protocol archaeology.

For Week 3, extract the mental model.

---

# Day 6 — caching guidance / reliability

## Azure Architecture Center — Caching guidance

https://learn.microsoft.com/en-us/azure/architecture/best-practices/caching

Read for:

- when caching is effective,
- concurrency,
- eventual consistency,
- reliability tradeoffs.

## Azure Architecture Center — No-Caching antipattern

https://learn.microsoft.com/en-us/azure/architecture/antipatterns/no-caching/

Useful because it also discusses the opposite risk:

When a cache fails, uncontrolled fallback can overwhelm the original data store.

---

# Day 7 — URL shortener

There is no single official architecture for a URL shortener.

Use the capstone as an original design exercise.

Good external worked examples can be consulted **after** your first attempt.

Recommended interview companion:

## System Design Interview — An Insider's Guide, Volume 1

Alex Xu.

Use the URL-shortener example only after writing your own design.

Process:

```text
1. Hide published solution.
2. Design your own.
3. Read the worked solution.
4. Record three differences.
5. Decide which differences are requirement-driven.
```

Never memorize their boxes.

---

# Books

## Designing Data-Intensive Applications, 2nd Edition

Martin Kleppmann & Chris Riccomini — O'Reilly, 2026

https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/

Week 3 use:

- derived/secondary data thinking,
- caches as copies,
- partitioning/hotspot intuition,
- failure and consistency reasoning.

Do not hunt for a chapter titled "Redis."

Use DDIA to strengthen the mental models behind the cache.

---

## Redis in Action

Josiah L. Carlson — Manning.

Older, but still useful for understanding Redis usage patterns and data structures.

Treat commands/configuration as version-sensitive.

Use current Redis docs to verify operational details.

---

## Designing Distributed Systems

Brendan Burns — O'Reilly.

Useful as a pattern-oriented companion for:

- replicated/distributed components,
- sidecars/ambassadors,
- distributed application structure.

Not Redis-specific.

---

# Suggested daily reading

```text
Day 1
  Core: Redis cache-aside overview
  Deep: Redis latency guide

Day 2
  Core: Azure Cache-Aside pattern
  Deep: Redis cache-aside production guidance

Day 3
  Core: TTL + EXPIRE + Key eviction
  Deep: Redis memory/eviction docs

Day 4
  Core: Hot keys docs
  Deep: cache-aside stampede discussion

Day 5
  Core: Redis Cluster specification — overview + key distribution
  Deep: hash tags + failover/resharding sections

Day 6
  Core: Caching guidance
  Deep: No-Caching antipattern

Day 7
  No new reading before the design.
  Design first.
  Compare with a worked URL-shortener example afterward.
```

---

# Reading rule

Whenever a source says:

```text
"Use X"
```

rewrite it as:

```text
"X is useful when ______ because ______,
but it creates ______."
```

That single exercise turns documentation into system-design knowledge.
