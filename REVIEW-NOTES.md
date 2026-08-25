# Week 1 Content Review — v1 → v2

## What was already good

The original module had a strong instructional skeleton:

- explicit learning outcomes,
- timeboxed lessons,
- Mermaid diagrams,
- "Break it" failure exercises,
- retrieval quizzes,
- a final design lab,
- repeated emphasis on tradeoffs over buzzwords.

Those are worth preserving.

## What was too light

### 1. Concepts stopped at first-order definitions

Examples:

- latency vs throughput did not yet cover percentiles/concurrency/saturation,
- HTTP did not yet connect idempotency to application retry design deeply enough,
- DNS/CDN did not cover record types/cache keys/revalidation,
- networking did not cover QUIC, SSE, WebSocket scaling, or backpressure,
- load balancing did not cover L4/L7, draining, failure domains, or downstream connection amplification.

### 2. Too few external sources

A technical course should teach learners how to verify claims against:

- RFCs,
- official documentation,
- production engineering literature.

Every day now includes curated sources.

### 3. The design lab needed measurable targets

The first design lab had good questions but not enough:

- SLOs,
- p50/p95/p99,
- back-of-the-envelope capacity,
- observability metrics,
- load-test design,
- cost discussion,
- scoring rubric.

Those have been added.

### 4. Review needed stronger retrieval practice

The quiz is expanded from 20 to 40 questions plus scenario drills, oral defense, and spaced repetition.

## Deliberately still out of scope

Week 1 does **not** attempt to fully teach:

- cryptography,
- BGP,
- DNSSEC,
- TCP congestion-control algorithms,
- Kubernetes,
- Kafka,
- database internals,
- multi-region consensus.

Those topics become useful later. Adding them now would increase vocabulary faster than understanding.

## Editorial standard for future weeks

Every lesson should contain:

1. Goal
2. Mental model
3. Core explanation
4. Concrete example
5. Architecture diagram
6. Tradeoff
7. Failure mode
8. Practical exercise
9. Retrieval questions
10. Exit criterion
11. Primary sources
12. Deep-dive reading

Every design lab should additionally contain:

- requirements,
- scale assumptions,
- SLOs,
- rough estimation,
- baseline architecture,
- bottleneck analysis,
- scaling path,
- failure matrix,
- observability,
- cost,
- tradeoffs,
- review rubric.
