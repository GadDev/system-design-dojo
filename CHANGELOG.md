# system-design-dojo

## 0.2.0

### Minor Changes

- fe381e3: Add Week 3: caching — cache fundamentals and Redis, cache-aside and key design, TTL/eviction/invalidation, stampede and hot-key handling, distributed caching with Redis Cluster, reliability/observability, the URL shortener design lab, a local Redis lab, and the week's review/quiz and resources.
- 90dcb1e: Add Week 9: consistency, event-driven architecture, and sagas — event-driven architecture and consistency (commands vs events, pub/sub vs work queues, eventual consistency), sagas/compensation/source of truth/reconciliation, the transcription platform design lab, optimistic locking/replica lag/reconciliation/saga lab simulations, a source-of-truth matrix template, and the week's reading map and review quiz.
- fe381e3: Add Week 2: databases — SQL vs NoSQL, keys/relationships/constraints, indexes and query plans, transactions/ACID/MVCC, connection pooling, replication/partitioning/sharding, the transcription data design lab, a local Postgres lab, and the week's review/quiz and resources.
- fe381e3: Add Week 1: foundations — request lifecycle, HTTP/HTTPS, DNS/CDN, TCP/UDP/WebSockets, load balancing and statelessness, the users API design lab, and the week's review/quiz and resources.
- fe381e3: Add Week 4: horizontal scaling — horizontal vs vertical scaling and statelessness, load balancing/health checks/sticky sessions, autoscaling and capacity signals, rate limiting and quotas, backpressure and load shedding, the 10,000 simultaneous uploads design lab with a FastAPI/NGINX scaling demo, k6 load test, and the week's review/quiz and resources.
- 83c8706: Add Week 8: observability — the stuck jobs incident lab, the observability review and incident defense exercises, an incident investigation template, a local observability stack (FastAPI, Prometheus, Grafana, OpenTelemetry) with sample events and analysis script, a reading map, and the week's review quiz.
- fe381e3: Add Week 6: distributed processing — fan-out/fan-in, work partitioning, job orchestration, race conditions/idempotency, orchestration tools (DB+Queue, Celery, Temporal, Step Functions), and the 90-minute transcription design lab.
- fe381e3: Add Week 5: queues and workers — queue mental model, delivery semantics/acks/ordering, idempotency and the outbox pattern, Redis vs RabbitMQ vs Kafka, retries/DLQ/poison messages, the async transcription queue design lab, Kafka/RabbitMQ/Redis Streams labs, a queue capacity calculator, and the week's review/quiz and resources.
- 29e3a36: Add Week 7: reliability — the transcription reliability playbook, the chaos design lab, a failure matrix template and game-day template, retry/circuit-breaker/fault-injection/health-check lab scripts, a reliability reading map, and the week's review/quiz.

### Patch Changes

- fe381e3: Add pnpm workspace configuration to allow esbuild builds.
