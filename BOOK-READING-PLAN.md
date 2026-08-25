# Book Reading Plan — 12 Weeks

You are not trying to finish books. You are using them as **precision tools**.

## Primary spine

### Designing Data-Intensive Applications, 2nd Edition (2026)

Use throughout the roadmap.

| Roadmap topic | DDIA focus |
|---|---|
| Foundations / requirements | Chapters 1–2 |
| Databases | data models + storage/retrieval |
| Replication | replication chapter |
| Partitioning | sharding chapter |
| Transactions | transactions chapter |
| Distributed failure | trouble with distributed systems |
| Consistency | consistency and consensus |
| Batch/stream | later dataflow/streaming chapters |

## Networking spine

### Computer Networking: A Top-Down Approach, 9th Edition

Use heavily in Weeks 1 and 4.

Do not read every derivation. Prioritize:

- application layer,
- HTTP,
- DNS,
- CDN/content distribution,
- transport layer,
- TCP congestion/reliability,
- QUIC/HTTP/3.

## Production spine

### Google Site Reliability Engineering + Workbook

Use:

```text
Week 1  → monitoring + load balancing
Week 7  → handling overload / cascading failures
Week 8  → monitoring / SLO / troubleshooting
Week 12 → non-abstract design / review
```

## Interview practice spine

### System Design Interview Vol. 1 / Vol. 2

Treat these as worked examples.

For every published solution:

1. Hide the solution.
2. Design it yourself.
3. Read their design.
4. Write three differences.
5. Decide which difference is requirement-driven.

Never memorize the diagram.

---

# Week 2 — Database Reading Sprint

Use **Designing Data-Intensive Applications, 2nd Edition** as the conceptual companion and PostgreSQL 18 docs as the implementation reference.

```text
Day 1 → DDIA: data models
Day 2 → PostgreSQL: constraints / schema
Day 3 → DDIA: storage & retrieval + PostgreSQL indexes/EXPLAIN
Day 4 → DDIA: transactions + PostgreSQL MVCC/isolation
Day 5 → PgBouncer docs + connection saturation thinking
Day 6 → DDIA: replication + partitioning/sharding
Day 7 → no new reading; defend your own design
```

The goal is not page count. The goal is to connect each concept to one architecture decision in the transcription platform.
---

# Week 3 — Caching Reading Sprint

Use Redis documentation as the implementation reference and **Designing Data-Intensive Applications, 2nd Edition** as the conceptual companion.

```text
Day 1 → Redis cache-aside overview + latency guide
Day 2 → Cache-Aside pattern + key design / negative caching
Day 3 → Redis TTL, EXPIRE, eviction policies
Day 4 → Hot keys + cache-stampede mitigation
Day 5 → Redis Cluster key distribution, hash slots, failover
Day 6 → caching reliability / observability guidance
Day 7 → no new reading; design URL shortener first, compare afterward
```

DDIA focus for Week 3:

- caches as derived copies rather than sources of truth,
- working sets and access skew,
- partitioning/hotspot intuition,
- failure and consistency tradeoffs.

The goal is not Redis command memorization. Every reading should end with one sentence of the form:

> “This technique is useful when ___, because ___, but it creates ___.”

