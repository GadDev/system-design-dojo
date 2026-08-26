# Book Reading Plan — 12 Weeks

You are not trying to finish books. You are using them as **precision tools**.

## Primary spine

### Designing Data-Intensive Applications, 2nd Edition (2026)

Use throughout the roadmap.

| Roadmap topic              | DDIA focus                        |
| -------------------------- | --------------------------------- |
| Foundations / requirements | Chapters 1–2                      |
| Databases                  | data models + storage/retrieval   |
| Replication                | replication chapter               |
| Partitioning               | sharding chapter                  |
| Transactions               | transactions chapter              |
| Distributed failure        | trouble with distributed systems  |
| Consistency                | consistency and consensus         |
| Batch/stream               | later dataflow/streaming chapters |

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

## The goal is not page count. The goal is to connect each concept to one architecture decision in the transcription platform.

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

> “This technique is useful when **_, because _**, but it creates \_\_\_.”

---

# Week 4 — Horizontal Scaling Reading Sprint

Use **Google Site Reliability Engineering** and the **SRE Workbook** as the production spine, with NGINX/FastAPI/Kubernetes/Redis documentation as concrete implementation references.

```text
Day 1 → FastAPI deployment/worker model + Kubernetes horizontal-scaling introduction
Day 2 → NGINX load balancing + Kubernetes readiness/liveness/startup probes
Day 3 → Kubernetes HPA control-loop behavior and scaling metrics
Day 4 → Redis rate-limiter pattern + RFC 6585 429 + Envoy token-bucket model
Day 5 → Google SRE cascading failures + managing load + retry/backoff guidance
Day 6 → Cloudflare R2 multipart/direct-upload + presigned URL documentation
Day 7 → no new reading; design the 10k-upload architecture first
```

Book focus:

- **Site Reliability Engineering** → overload, cascading failures, load balancing, capacity.
- **The Site Reliability Workbook** → managing load in production.
- **Release It!, 2nd Edition** → stability, timeouts, bulkheads, overload mindset.
- **Computer Networking: A Top-Down Approach, 9th Edition** → transport/congestion context.
- **Designing Data-Intensive Applications, 2nd Edition** → distributed failure and shared-state reasoning.

Every reading should end with:

> “Which bottleneck or failure mode would make me use this technique?”

---

# Week 5 — Queues & Workers Reading Sprint

Use official broker documentation to learn the actual delivery mechanics, then use architecture books to generalize the patterns.

```text
Day 1 → FastAPI BackgroundTasks caveat + Redis/RabbitMQ consumer mental model
Day 2 → RabbitMQ reliability/ACKs + Kafka delivery semantics
Day 3 → PostgreSQL constraints/transactions recap + Transactional Outbox pattern
Day 4 → Redis Streams + RabbitMQ exchanges/queues + Kafka topics/partitions/groups
Day 5 → RabbitMQ DLX + Celery retry/backoff + Google SRE cascading-failure guidance
Day 6 → re-read FastAPI/Celery boundaries; apply everything to transcription
Day 7 → no new reading; defend your broker and delivery choices first
```

Book focus:

- **Designing Data-Intensive Applications, 2nd Edition** → dataflow, logs/streams, distributed failure, message-driven systems.
- **Enterprise Integration Patterns** → competing consumers, dead-letter channel, idempotent receiver, message routing vocabulary.
- **Release It!, 2nd Edition** → retry amplification, stability boundaries, overload and recovery.
- **Designing Event-Driven Systems** → Kafka/log-based event architecture and replay.

Every reading should end with two statements:

> “This mechanism gives me \_\_\_.”
>
> “It still leaves me responsible for \_\_\_.”

That second sentence is the important one in distributed systems.

---

# Week 6 — Distributed Processing Reading Sprint

Use the Google MapReduce paper for the foundational fan-out/fan-in mental model, framework documentation for concrete orchestration mechanisms, and DDIA for failure/coordination reasoning.

```text
Day 1 → Google MapReduce: map/reduce model, scheduling, failure handling
Day 2 → FFmpeg segment muxer + DDIA partitioning/failure-domain intuition
Day 3 → Celery groups/chords + Step Functions Map concurrency controls
Day 4 → revisit fan-in primitives; focus on barriers, ordering and stragglers
Day 5 → Redis distributed-lock caveats + PostgreSQL advisory locks
Day 6 → Temporal durable execution + Step Functions Distributed Map
Day 7 → no new reading; defend your own workflow before comparing tools
```

Book focus:

- **Designing Data-Intensive Applications, 2nd Edition** → partitioning, distributed failure, dataflow, coordination.
- **Designing Distributed Systems** → work queues, scatter/gather and orchestration patterns.
- **Enterprise Integration Patterns** → aggregator, correlation identifier, idempotent receiver.
- **Release It!, 2nd Edition** → tail latency, overload and failure amplification.

Every reading should end with:

> "What is the unit of work, what is the unit of failure, and what state lets the workflow recover?"

---

# Week 7 — Reliability Reading Sprint

Use AWS Builders' Library and Google SRE for retry/overload behavior, Kubernetes docs for health semantics, and PostgreSQL/Redis docs for concrete failover behavior.

```text
Day 1 → AWS timeout guidance + Google SRE cascading-failure model
Day 2 → AWS retries/backoff/jitter + safe-idempotent retries
Day 3 → Resilience4j circuit-breaker state machine + Release It!
Day 4 → Kubernetes startup/liveness/readiness + graceful degradation
Day 5 → PostgreSQL failover + Redis Sentinel + RTO/RPO reasoning
Day 6 → Cloudflare R2 error/retry docs + transcription recovery playbook
Day 7 → no new reading; execute the chaos design lab first
```

Book focus:

- **Release It!, 2nd Edition** → circuit breakers, bulkheads, stability boundaries, cascading failures.
- **Site Reliability Engineering** → overload, cascading failures, graceful degradation.
- **The Site Reliability Workbook** → operational practices, incident/game-day thinking.
- **Designing Data-Intensive Applications, 2nd Edition** → partial failure, replication, durability/availability tradeoffs.

Every reading should end with:

> “What fails, how do we contain it, and what evidence proves recovery?”

---

# Week 8 — Observability Reading Sprint

Use OpenTelemetry as the vendor-neutral instrumentation spine, Prometheus for metric semantics/querying, Grafana for visualization/correlation, and Google SRE for SLO/alerting reasoning.

```text
Day 1 → OpenTelemetry signals, logs and context propagation
Day 2 → Prometheus metric types, instrumentation, naming/cardinality, histograms
Day 3 → OpenTelemetry Python + Collector + W3C Trace Context
Day 4 → Google SRE SLO chapter + SRE Workbook Implementing SLOs
Day 5 → Grafana alerting/exemplars + Google SRE monitoring chapter
Day 6 → no broad reading first; execute the stuck-job incident lab, then compare with SRE alerting material
Day 7 → no new reading; defend your telemetry architecture and incident flow
```

Book focus:

- **Site Reliability Engineering** → monitoring distributed systems, SLOs, practical alerting.
- **The Site Reliability Workbook** → implementing SLOs, monitoring, alerting on SLOs.
- **Observability Engineering** → exploratory debugging, high-cardinality event data and observability practice.
- **Distributed Systems Observability** → compact logs/metrics/traces mental models.

Every reading should end with:

> “Which question does this signal answer quickly, and which question does it _not_ answer?”

---

# Week 9 — Consistency & Distributed Data Reading Sprint

Use PostgreSQL and RFC material for concrete concurrency/transaction semantics, CAP literature for partition reasoning, and architecture guidance for event-driven workflows and sagas.

```text
Day 1 → DDIA consistency/replication + PostgreSQL transaction isolation
Day 2 → Brewer/Gilbert-Lynch CAP + PostgreSQL logical replication/lag intuition
Day 3 → RFC 9110 If-Match + PostgreSQL concurrency-control docs
Day 4 → PostgreSQL 2PC / PREPARE TRANSACTION + distributed-transaction failure analysis
Day 5 → Azure Event-Driven Architecture + Kafka event/log concepts
Day 6 → AWS Saga patterns + Azure Compensating Transaction
Day 7 → no new reading; defend source-of-truth and reconciliation choices first
```

Book focus:

- **Designing Data-Intensive Applications, 2nd Edition** → replication, consistency, transactions, linearizability, dataflow.
- **Database Internals** → replication, distributed transactions and deeper storage mechanics.
- **Designing Event-Driven Systems** → event logs, streams, replay and event architecture.
- **Enterprise Integration Patterns** → idempotent receiver, aggregator, message sequence and correlation vocabulary.

Every reading should end with:

> “Which fact is authoritative, how stale may derived copies be, and how does the system converge after disagreement?”
