# Week 4 — Sources, Books & Reading Map

This is the curated bibliography for Week 4.

**Reference API:** FastAPI.

**Reference load balancer:** NGINX for local learning.

**Reference autoscaling model:** Kubernetes Horizontal Pod Autoscaler.

**Reference shared limiter/cache:** Redis.

**Reference object storage:** Cloudflare R2 for the transcription capstone.

**Verified for this course revision:** August 2026.

Priority:

1. protocol/project official documentation,
2. Google SRE / production engineering literature,
3. durable books,
4. vendor implementation examples,
5. interview material last.

---

# Day 1 — horizontal scaling + stateless services

## FastAPI — Containers / workers

https://fastapi.tiangolo.com/deployment/docker/

Read for:

- worker processes,
- replication concepts,
- memory/process tradeoffs,
- why deployment topology depends on environment.

Do not memorize “N workers per container.”

Understand the distinction between **process concurrency** and **service replication**.

## Kubernetes — Horizontal Pod Autoscaling

https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/

Read the introduction for:

- horizontal vs vertical scaling,
- scaling a workload by replica count,
- custom/resource metrics.

Day 3 will revisit this in more depth.

---

# Day 2 — load balancing + health

## NGINX — HTTP Load Balancing

https://nginx.org/en/docs/http/load_balancing.html

Required concepts:

- round robin,
- least connected,
- IP hash/session persistence,
- weighted balancing,
- passive health behavior.

Use NGINX as a concrete implementation, not as the definition of load balancing itself.

## Kubernetes — Liveness, Readiness, Startup Probes

https://kubernetes.io/docs/concepts/workloads/pods/probes/

Read for:

- why readiness controls traffic eligibility,
- why liveness and readiness have different purposes,
- startup behavior.

Key question:

> Is this instance alive, or is it safe to send it new work?

Those are not identical questions.

---

# Day 3 — autoscaling

## Kubernetes — Horizontal Pod Autoscaling

https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/

Required.

Focus on:

- control loop,
- metric sources,
- desired/current metric ratio,
- readiness/startup effects,
- scale-up/down behavior,
- stabilization.

Do not over-focus on YAML.

Extract the systems mental model.

## Kubernetes — HPA walkthrough

https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/

Optional hands-on follow-up.

---

# Day 4 — rate limiting

## Redis — `INCR` rate limiter pattern

https://redis.io/docs/latest/commands/incr/

Read the rate-limiter pattern for:

- counters,
- expiry,
- atomicity concerns.

Redis may add newer commands over time; the lasting concept is atomic shared state for a distributed limiter.

## Envoy — Token Bucket

https://www.envoyproxy.io/docs/envoy/latest/api-v3/type/v3/token_bucket.proto

Read for the canonical configuration concepts:

```text
max tokens
refill amount
fill interval
```

## Envoy — local rate limit

https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/local_rate_limit_filter.html

Read for:

- local token-bucket enforcement,
- 429 behavior,
- per-process/per-connection scope.

## Envoy — global rate limiting overview

https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/other_features/global_rate_limiting.html

Useful for understanding:

```text
local coarse protection
+
global policy
```

## RFC 6585 — 429 Too Many Requests

https://www.rfc-editor.org/rfc/rfc6585.html

Read Section 4.

Focus on:

- meaning of `429`,
- optional `Retry-After`,
- standard intentionally does not mandate one rate-limit algorithm.

---

# Day 5 — overload + backpressure

## Google SRE — Addressing Cascading Failures

https://sre.google/sre-book/addressing-cascading-failures/

Strongly recommended.

Focus on:

- load shedding,
- queue management,
- overload propagation,
- retries as additional traffic.

## Google SRE Workbook — Managing Load

https://sre.google/workbook/managing-load/

Focus on the relationship between:

```text
load balancing
autoscaling
load shedding
```

and why they must be designed together.

## Google SRE — Production Services Best Practices

https://sre.google/sre-book/service-best-practices/

Read the overload/failure guidance.

Important themes:

- load testing,
- graceful degradation,
- load shedding,
- exponential backoff + jitter.

## AWS Well-Architected — Control and limit retry calls

https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_limit_retries.html

Read for:

- retry storms,
- retries at multiple layers,
- backoff,
- jitter,
- max retry budgets.

Use as implementation/production guidance, not as AWS-specific architecture dogma.

---

# Day 6–7 — direct video upload / R2

## Cloudflare R2 — Upload Objects

https://developers.cloudflare.com/r2/objects/upload-objects/

Current R2 guidance explicitly distinguishes:

- single upload for smaller objects,
- multipart for large/resumable/parallel uploads.

Read for:

- direct client upload,
- multipart advantages,
- bounded part size/concurrency thinking.

## Cloudflare R2 — Presigned URLs

https://developers.cloudflare.com/r2/api/s3/presigned-urls/

Read for:

- temporary scoped operations,
- browser direct uploads,
- expiry,
- bearer-token security model,
- CORS/content-type considerations.

## Cloudflare R2 — Limits

https://developers.cloudflare.com/r2/platform/limits/

Use only when implementing against R2.

Provider limits change.

System-design principle:

> Put provider-specific limits in implementation/configuration decisions, not in universal architecture assumptions.

---

# Books

## Site Reliability Engineering

Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy — Google/O'Reilly.

Free online:

https://sre.google/sre-book/table-of-contents/

Week 4 focus:

- load balancing,
- cascading failures,
- overload,
- production best practices.

## The Site Reliability Workbook

Google/O'Reilly.

Free online:

https://sre.google/workbook/table-of-contents/

Week 4 focus:

- managing load,
- practical operational patterns.

## Release It!, 2nd Edition

Michael T. Nygard.

Week 4 focus:

- stability patterns,
- timeouts,
- bulkheads,
- circuit-breaker mindset,
- capacity/failure thinking.

You do not need to implement every pattern this week.

Use the book to develop the habit:

> “How does this service behave when dependencies are slow or full?”

## Designing Data-Intensive Applications, 2nd Edition

Martin Kleppmann & Chris Riccomini — O'Reilly, 2026.

https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/

Week 4 use:

- distributed-system failure mindset,
- partitioning/hotspot intuition,
- throughput/latency tradeoffs,
- architecture decisions around shared state.

DDIA is not a load-balancer manual.

Use it to strengthen reasoning, not implementation commands.

## Computer Networking: A Top-Down Approach, 9th Edition

James Kurose & Keith Ross.

Week 4 focus:

- transport behavior,
- congestion concepts,
- application/network boundary,
- content distribution/load concepts where relevant.

---

# Suggested reading schedule

```text
Day 1
→ FastAPI deployment workers
→ Kubernetes HPA introduction

Day 2
→ NGINX load balancing
→ Kubernetes probes

Day 3
→ Kubernetes HPA deeper reading

Day 4
→ Redis INCR limiter
→ RFC 6585 section 4
→ Envoy token bucket/local/global limiter overview

Day 5
→ Google SRE cascading failures
→ Google SRE managing load
→ AWS retry/backoff guidance

Day 6
→ Cloudflare R2 upload objects + presigned URLs

Day 7
→ no new reading until after your design
```

Capstone rule:

> Design first. Compare with external material second.
