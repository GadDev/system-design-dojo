# System Design Bible / Notebook 🧠📓

This file is the index for your personal system-design notebook.

The goal is not to collect definitions. It is to build **retrievable decision knowledge**.

Use [`week-11-system-design-interview/design-notebook-template.md`](week-11-system-design-interview/design-notebook-template.md) for every concept.

---

## Suggested pages

### Foundations

- DNS
- CDN
- HTTP / idempotency
- WebSocket
- Load balancer

### Data

- PostgreSQL
- Index
- Transaction / MVCC
- Read replica
- Partitioning
- Sharding

### Caching

- Redis
- Cache-aside
- TTL
- Hot key
- Stampede

### Scale / async

- Rate limiting
- Backpressure
- Queue
- Worker
- DLQ
- Outbox

### Distributed processing

- Fan-out / fan-in
- Idempotency
- Distributed lock
- Saga
- Reconciliation

### Reliability / operations

- Timeout
- Retry + jitter
- Circuit breaker
- SLO
- Logs
- Metrics
- Traces

### Architecture

- Modular monolith
- Microservices
- Event-driven architecture
- CQRS
- Event sourcing

---

# Example — Redis

## Problem it solves

Fast shared access to hot/ephemeral state when repeatedly hitting the authoritative database would be slower or more expensive.

## Typical uses

- cache,
- rate limiting,
- transient shared state,
- some queue/stream workloads.

## Tradeoffs

- memory is expensive,
- cache invalidation,
- hot keys,
- distributed failure modes,
- persistence/HA semantics differ from a relational DB.

## When NOT to use it

When indexed PostgreSQL comfortably handles the workload and adding a distributed cache would only introduce another consistency/failure boundary.

## Transcription example

Potentially useful for rate limiting and short-lived cached job reads; not automatically required as authoritative job storage.

---

# Review rhythm

For every page:

```text
Day 0 → create it
Day 2 → explain without notes
Day 7 → answer failure/tradeoff questions
Day 30 → decide whether you still remember when NOT to use it
```
