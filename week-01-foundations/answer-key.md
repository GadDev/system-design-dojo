# Week 1 — Answer Key

> Open this only after completing Day 7 from memory.

These are **reference answers**, not scripts to memorize. Many system-design questions allow multiple defensible answers.

## 1–20

1. **Latency:** elapsed time for an operation/request from the chosen measurement boundary.
2. **Throughput:** amount of work completed per unit time.
3. Network/DNS/TLS/downstream/database/queueing costs can dominate API execution time.
4. Examples: DNS, edge/CDN, load balancer, API, cache, database, downstream network.
5. `202 Accepted` says work was accepted but is not complete; useful for asynchronous processing.
6. Idempotency means repeating the intended request has the same intended effect as doing it once.
7. They allow duplicate/retried non-idempotent-looking requests to map to one logical operation.
8. `401`: authentication required/invalid. `403`: identity may be known but is not allowed.
9. Confidentiality, integrity, and endpoint/server authentication at the simplified Week 1 level.
10. DNS lets clients resolve names to information needed to reach services.
11. How long cached DNS data may be reused before refresh.
12. Requested content is already present in the relevant CDN cache.
13. The URL changes with content version, so old and new assets can safely coexist.
14. It can leak one user's data to another or serve incorrect personalized content.
15. Reliable ordered byte-stream semantics.
16. Simplicity/stateless request handling/easier recovery.
17. Low-latency server push or bidirectional communication.
18. It distributes incoming work across backend instances.
19. Any instance can handle the next request without hidden local conversational state.
20. Skew, coupling to instances, harder failover.

## 21–40

21. p50 is median; p99 describes the slow tail.
22. Each replica may create its own connections/queries, multiplying downstream load.
23. A DNS service that performs resolution on behalf of the client and caches results.
24. Examples: A→IPv4, AAAA→IPv6, CNAME→alias, MX→mail, TXT→text/policy, NS→nameserver.
25. Freshness controls reuse without checking; validation checks whether cached content remains current.
26. Distinct responses may collapse into one cache entry, causing incorrect or unsafe content delivery.
27. `POST` is generally not idempotent by method semantics, but an application can define a safe retry mechanism such as idempotency keys.
28. It maps retries/duplicates to one logical operation/result.
29. It avoids holding a request open for long-running work and gives the client a status-monitor pattern.
30. Handling a producer that can emit data faster than the consumer can process.
31. Connections can drop and events can be missed; durable job state must survive transport loss.
32. One-way server-to-client event streams such as notifications or progress.
33. HTTP/3 uses QUIC over UDP, changing connection/stream behavior while QUIC implements reliability and security properties needed by HTTP.
34. A process can be alive but temporarily unable to safely receive traffic.
35. Stop new traffic, allow in-flight work to finish, then terminate an instance.
36. State exists elsewhere; the instance simply avoids depending on unique local state across requests.
37. A set of components likely to fail together because they share infrastructure/dependency boundaries.
38. Latency, traffic, errors, saturation.
39. DB read pressure/saturation, high repeated-key locality, latency target misses, and an acceptable staleness model.
40. Low hit ratio, higher latency, stale-data incidents, excessive complexity/cost, cache outages causing harmful stampedes.

## Scenario guidance

### Mysterious slowdown

Investigate:

- DB query latency,
- connection-pool wait,
- downstream calls,
- lock contention,
- network errors/retransmissions,
- queue depth,
- GC/runtime pauses,
- request mix.

Do not jump straight to “add servers.”

### Redis disappeared

Correctness should survive if Redis is only a cache. Protect PostgreSQL from a sudden miss storm with techniques such as bounded concurrency, request coalescing/single-flight, staggered TTLs, stale serving where safe, and gradual recovery.

### Realtime progress

Store authoritative progress durably. On reconnect, fetch the latest state and resume live updates. Intermediate percentage events usually do not need durable replay unless the product explicitly requires an audit/event log.
