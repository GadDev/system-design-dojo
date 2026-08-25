# 🗺️ 12-Week System Design Roadmap

This roadmap is intentionally cumulative: every week adds one new layer to the same mental model.

---

## Week 1 — Request Lifecycle & Web Foundations

**Outcome:** Trace a request from browser to backend and explain where latency, scaling, and failure can appear.

| Day | Topic | Deliverable |
|---|---|---|
| 1 | The full request lifecycle | Draw browser → DNS → CDN → LB → API → DB |
| 2 | HTTP & HTTPS | Explain methods, status codes, headers, TLS, keep-alive |
| 3 | DNS & CDN | Explain resolution, TTL, caching, edge delivery |
| 4 | TCP, UDP & WebSockets | Compare transport choices and persistent connections |
| 5 | Reverse proxies, load balancers & stateless APIs | Scale one API instance to many |
| 6 | Design lab: `GET /users/:id` at 10M users | Full mini design review |
| 7 | Retrieval practice + quiz | One-page architecture recap |

---

## Week 2 — Databases & Storage

**Outcome:** Design a PostgreSQL persistence model from access patterns, protect invariants under concurrency, and choose the correct database scaling mechanism from evidence rather than habit.

| Day | Topic | Deliverable |
|---|---|---|
| 1 | SQL vs NoSQL + workload-first modeling | Storage decision matrix |
| 2 | Primary keys, foreign keys & constraints | Transcription ER model |
| 3 | Indexes & query plans | Query-driven index plan + EXPLAIN lab |
| 4 | Transactions, ACID, MVCC & isolation | Safe chunk/job state transition |
| 5 | Connections & pooling | Connection-pressure analysis |
| 6 | Replication, read replicas, partitioning & sharding | Database scaling decision tree |
| 7 | Transcription data design lab + review | Full database design review + transcript storage ADR |

---

## Week 3 — Caching with Redis

**Outcome:** Reduce latency and database load while reasoning explicitly about freshness, invalidation, memory, hot keys, stampedes, and distributed-cache failure.

| Day | Topic | Deliverable |
|---|---|---|
| 1 | Cache fundamentals + Redis mental model | Cache suitability matrix |
| 2 | Cache-aside, hits, misses & key design | Working cache-aside flow |
| 3 | TTL, expiration, eviction & invalidation | Freshness policy |
| 4 | Stampedes, hot keys & negative caching | Failure mitigation playbook |
| 5 | Distributed caching & Redis Cluster | Distributed-cache architecture |
| 6 | Reliability, observability & transcription cache review | Cache design review |
| 7 | Design lab: URL shortener | API + DB + Redis + edge-cache design |

---

## Week 4 — Scaling Stateless Services

**Outcome:** Scale a service horizontally and reason about the new bottlenecks created by scaling.

| Day | Topic | Deliverable |
|---|---|---|
| 1 | Vertical vs horizontal scaling | Decision table |
| 2 | Load balancing strategies | Round-robin / least-connections / hashing |
| 3 | Statelessness & sessions | Externalized session design |
| 4 | Autoscaling & capacity | Scaling signals and thresholds |
| 5 | Backpressure & admission control | Overload protection plan |
| 6 | Design lab: 10k simultaneous video uploads | Bottleneck map |
| 7 | Review | 10× / 100× / 1000× exercise |

---

## Week 5 — Queues & Asynchronous Work

**Outcome:** Design long-running work without blocking request/response APIs.

| Day | Topic | Deliverable |
|---|---|---|
| 1 | Producer/consumer model | Basic queue architecture |
| 2 | Delivery semantics | At-most / at-least / effectively-once |
| 3 | Idempotency | Idempotent job handler |
| 4 | Redis, RabbitMQ, Kafka | Selection matrix |
| 5 | Dead-letter queues & retries | Failure policy |
| 6 | Design lab: async transcription | Upload → queue → worker flow |
| 7 | Review | Explain why “exactly once” is tricky |

---

## Week 6 — Distributed Processing & Orchestration

**Outcome:** Split large workloads into safe, parallel sub-jobs.

| Day | Topic | Deliverable |
|---|---|---|
| 1 | Fan-out / fan-in | Chunk processing diagram |
| 2 | Work partitioning | Chunk-size strategy |
| 3 | Concurrency limits | Per-user / global concurrency rules |
| 4 | Aggregation & ordering | Merge algorithm |
| 5 | Race conditions & distributed locks | Failure scenarios |
| 6 | Design lab: 2-hour video pipeline | Parent/child job model |
| 7 | Review | Rebuild the pipeline from memory |

---

## Week 7 — Reliability Engineering

**Outcome:** Treat failure as a normal operating condition.

| Day | Topic | Deliverable |
|---|---|---|
| 1 | Timeouts | Timeout budget |
| 2 | Retries & exponential backoff | Retry policy |
| 3 | Circuit breakers | Dependency protection flow |
| 4 | Graceful degradation | Reduced-functionality mode |
| 5 | Failover & health checks | Recovery strategy |
| 6 | Chaos lab: destroy the transcription system | Failure matrix |
| 7 | Review | Reliability checklist |

---

## Week 8 — Observability

**Outcome:** Diagnose a production incident from signals rather than guesses.

| Day | Topic | Deliverable |
|---|---|---|
| 1 | Structured logs | Logging schema |
| 2 | Metrics | Golden signals dashboard plan |
| 3 | Distributed tracing | Request trace |
| 4 | SLI / SLO / SLA | Initial SLOs |
| 5 | Alerting | Actionable alert rules |
| 6 | Incident lab: “job stuck for 30 minutes” | Investigation playbook |
| 7 | Review | Observability scorecard |

---

## Week 9 — Consistency & Distributed Data

**Outcome:** Choose consistency guarantees consciously.

| Day | Topic | Deliverable |
|---|---|---|
| 1 | Strong vs eventual consistency | Use-case comparison |
| 2 | CAP theorem | Practical failure examples |
| 3 | Optimistic concurrency | Versioned update example |
| 4 | Distributed transactions | Why 2PC is costly |
| 5 | Sagas & compensation | Multi-step workflow |
| 6 | Design lab: worker finished but DB update failed | Source-of-truth decision |
| 7 | Review | Consistency decision tree |

---

## Week 10 — Architecture Patterns

**Outcome:** Recognize architecture patterns as tools, not goals.

| Day | Topic | Deliverable |
|---|---|---|
| 1 | Modular monolith | Module boundaries |
| 2 | Microservices | Extraction criteria |
| 3 | Event-driven architecture | Event flow |
| 4 | CQRS | Read/write split example |
| 5 | Event sourcing | When it helps / hurts |
| 6 | Design lab: evolve transcription app | Monolith → selected services |
| 7 | Review | Pattern decision matrix |

---

## Week 11 — System Design Interview Mechanics

**Outcome:** Produce a coherent design under time pressure.

| Day | Topic | Deliverable |
|---|---|---|
| 1 | Requirement clarification | Question checklist |
| 2 | Back-of-envelope estimation | QPS/storage worksheet |
| 3 | API design | Stable API contract |
| 4 | Data model | Access-pattern-first schema |
| 5 | Bottleneck analysis | 10× scale analysis |
| 6 | Mock design: notification system | 45-minute design |
| 7 | Review | Self-score rubric |

---

## Week 12 — Capstone & Mastery

**Outcome:** Defend a production-grade design and its tradeoffs end to end.

| Day | Topic | Deliverable |
|---|---|---|
| 1 | Design YouTube-lite | Media architecture |
| 2 | Design chat | Realtime architecture |
| 3 | Design feed | Fan-out tradeoffs |
| 4 | Design Dropbox-lite | Sync + consistency |
| 5 | Final transcription architecture | Complete architecture |
| 6 | 100k hours/day scaling challenge | Capacity + cost + failure review |
| 7 | Portfolio review | Publishable system-design case study |

---

# Graduation criteria 🥷

You are ready to call the first stage complete when you can design an unfamiliar system and naturally move through:

```text
Requirements → Estimates → API → Data → Architecture → Scale → Failure → Security → Cost → Tradeoffs
```

The key signal is not naming more technologies. It is being able to explain **why a component exists, which requirement it satisfies, and what new failure mode it introduces**.
