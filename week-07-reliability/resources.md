# Week 7 — Sources & Reading Map

Use primary documentation and production engineering material first. This week is about failure behavior that has been learned the expensive way in real systems.

---

# Day 1–2 — Timeouts, Retries, Backoff & Jitter

## Amazon Builders' Library — Timeouts, retries, and backoff with jitter

https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/

Read for:

- why every remote call needs bounded waiting,
- connection vs request timeout intuition,
- why retries increase backend load,
- capped exponential backoff,
- jitter,
- retrying idempotent operations safely.

Write after reading:

```text
A retry improves availability when:
A retry makes an outage worse when:
```

## Amazon Builders' Library — Making retries safe with idempotent APIs

https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/

Read for:

- ambiguous remote outcomes,
- client request identifiers,
- why retryable mutations need idempotent semantics.

## Google SRE — Addressing Cascading Failures

https://sre.google/sre-book/addressing-cascading-failures/

Read for:

- overload cascades,
- retry amplification,
- randomized exponential backoff,
- graceful degradation/load shedding.

## Google SRE — Production Services Best Practices

https://sre.google/sre-book/service-best-practices/

Focus on:

- overload behavior,
- degraded results,
- traffic dropping/load shedding,
- backoff with jitter.

---

# Day 3 — Circuit Breakers

## Resilience4j — CircuitBreaker

https://resilience4j.readme.io/docs/circuitbreaker

Use it as a concrete implementation of the pattern.

Focus on:

- CLOSED / OPEN / HALF_OPEN,
- count/time sliding windows,
- failure rate,
- slow-call rate,
- minimum sample size,
- controlled calls in half-open state.

Important:

> A circuit breaker does not itself limit concurrency. That is a bulkhead/concurrency-control concern.

## Release It!, 2nd Edition — Michael Nygard

Read sections around:

- circuit breaker,
- bulkheads,
- cascading failures,
- stability patterns.

Do not memorize pattern names. Ask which failure amplification each pattern prevents.

---

# Day 4 — Health Checks & Graceful Degradation

## Kubernetes — Liveness, Readiness, and Startup Probes

https://kubernetes.io/docs/concepts/workloads/pods/probes/

Read carefully for:

- liveness → restart decision,
- readiness → receive traffic decision,
- startup → initialization protection,
- why bad liveness probes can cause cascading failures,
- probe failure thresholds/timeouts.

Then answer:

```text
Should PostgreSQL being down make my FastAPI process “not live”?
```

There is no universal answer, but for most APIs the answer is **not automatically**.

## Google SRE — Production Services Best Practices

Re-read graceful degradation / overload sections.

---

# Day 5 — Failover & Stateful Recovery

## PostgreSQL 18 — High Availability, Load Balancing and Replication

https://www.postgresql.org/docs/18/high-availability.html

## PostgreSQL 18 — Failover

https://www.postgresql.org/docs/18/warm-standby-failover.html

Read for:

- standby promotion,
- old-primary fencing / STONITH problem,
- failover vs restoring redundancy,
- operational testing.

## Redis — High availability with Redis Sentinel

https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/

Read for:

- monitoring,
- objective failure detection,
- failover coordination,
- replica promotion,
- client configuration discovery,
- asynchronous-replication data-loss caveat.

Important:

```text
Automatic failover ≠ zero RPO.
```

---

# Day 6–7 — Provider Failure / Game Days

## Cloudflare R2 — Error codes

https://developers.cloudflare.com/r2/api/error-codes/

Read for current concrete behavior:

- `500 InternalError` → retry,
- `503 ServiceUnavailable` → exponential backoff,
- `429 TooManyRequests` → rate-limit behavior,
- multipart-specific errors,
- auth/validation failures that should not be blindly retried.

## Cloudflare R2 — Troubleshooting 5xx / capacity

https://developers.cloudflare.com/r2/platform/troubleshooting/

Read for:

- concurrent-request pressure,
- retry behavior,
- slowing clients collectively,
- bucket sharding as a provider-specific capacity mitigation.

Provider docs can change. Treat these as **current implementation facts**, not universal distributed-systems laws.

---

# Books

## Site Reliability Engineering — Google

Free online:

https://sre.google/sre-book/table-of-contents/

Week 7 focus:

- Addressing Cascading Failures,
- Handling Overload,
- Managing Critical State / reliability-related chapters as relevant.

## The Site Reliability Workbook — Google

https://sre.google/workbook/table-of-contents/

Use for operationalizing reliability ideas and incident/game-day thinking.

## Release It!, 2nd Edition — Michael T. Nygard

Best companion book for this week.

Focus on:

- stability patterns,
- timeouts,
- circuit breakers,
- bulkheads,
- integration points,
- cascading failure.

## Designing Data-Intensive Applications, 2nd Edition

Use for:

- partial failures,
- distributed coordination,
- replication/failover tradeoffs,
- durability vs availability.

---

# Suggested reading schedule

```text
Day 1 → AWS timeout sections + Google SRE cascading failures
Day 2 → AWS retries/backoff/jitter + idempotent API article
Day 3 → Resilience4j circuit-breaker model + Release It! stability patterns
Day 4 → Kubernetes probes + Google SRE graceful degradation
Day 5 → PostgreSQL failover + Redis Sentinel
Day 6 → Cloudflare R2 error/retry docs + reread your Week 5/6 failure semantics
Day 7 → no new reading; run the design lab before checking notes
```

---

# Source-evaluation rule

For every reliability mechanism, write:

```text
Failure it addresses:
Failure it does NOT address:
New failure mode it introduces:
Evidence that it is working:
```

Example:

```text
Mechanism: Circuit breaker
Addresses: repeatedly calling an unhealthy dependency
Does not address: duplicate side effects
Introduces: false opens / stale breaker state / recovery tuning
Evidence: lower failed downstream attempts, controlled half-open recovery, stable queue age
```
