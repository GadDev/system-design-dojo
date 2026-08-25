# Week 1 — Sources, Books & Reading Map

This file is the curated bibliography for Week 1.

**Rule:** primary sources before summaries.

> Verified for this course revision: August 2026.

---

# 1. Standards

## HTTP

### RFC 9110 — HTTP Semantics
https://www.rfc-editor.org/rfc/rfc9110.html

Use for:

- method semantics,
- safe/idempotent methods,
- status-code semantics,
- HTTP terminology.

Do not read front-to-back during Week 1. Search the RFC when a precise semantic question appears.

## TLS

### RFC 8446 — TLS 1.3
https://www.rfc-editor.org/rfc/rfc8446.html

Use for:

- modern TLS terminology,
- handshake/security model.

## TCP

### RFC 9293 — Transmission Control Protocol
https://www.rfc-editor.org/rfc/rfc9293.html

This is the modern TCP base specification and obsoletes RFC 793 as the normative TCP specification.

## UDP

### RFC 768 — User Datagram Protocol
https://www.rfc-editor.org/rfc/rfc768.html

Short enough to inspect directly.

## WebSocket

### RFC 6455 — The WebSocket Protocol
https://www.rfc-editor.org/rfc/rfc6455.html

Use when you want protocol-level details beyond the browser API.

---

# 2. Web Platform References

## MDN — HTTP
https://developer.mozilla.org/en-US/docs/Web/HTTP

Recommended pages:

- Overview of HTTP  
  https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview

- Request methods  
  https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods

- Status codes  
  https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status

- HTTP caching  
  https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching

## MDN — WebSocket API
https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API

Good bridge between browser usage and protocol concepts.

---

# 3. DNS & CDN

## Cloudflare — What is DNS?
https://www.cloudflare.com/learning/dns/what-is-dns/

## Cloudflare — What is caching?
https://www.cloudflare.com/learning/cdn/what-is-caching/

## Cloudflare Cache docs
https://developers.cloudflare.com/cache/get-started/

Why these are included:

- clear explanations,
- concrete edge-cache behavior,
- useful operational vocabulary.

Remember that Cloudflare docs describe Cloudflare's product behavior in addition to general concepts.

---

# 4. Reliability & Production Engineering

## Google — Site Reliability Engineering
https://sre.google/books/

The books are legally available to read online from Google.

### Monitoring Distributed Systems
https://sre.google/sre-book/monitoring-distributed-systems/

Week 1 takeaway:

```text
latency
traffic
errors
saturation
```

### Service Level Objectives
https://sre.google/sre-book/service-level-objectives/

### Load Balancing at the Frontend
https://sre.google/sre-book/load-balancing-frontend/

### Load Balancing in the Datacenter
https://sre.google/sre-book/load-balancing-datacenter/

### Handling Overload
https://sre.google/sre-book/handling-overload/

## Site Reliability Workbook
https://sre.google/workbook/table-of-contents/

Especially useful later for hands-on production thinking.

---

# 5. Concrete Load-Balancer Documentation

## AWS — Elastic Load Balancing concepts
https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html

Use it to see:

- targets,
- listeners,
- health checks,
- routing,
- availability concepts.

Treat it as an implementation example, not universal architecture law.

## NGINX — Reverse Proxy
https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/

Useful for seeing what a reverse proxy actually does in a familiar production tool.

---

# 6. Books

## Designing Data-Intensive Applications, 2nd Edition

**Martin Kleppmann & Chris Riccomini — O'Reilly, February 2026**

https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/

Best for:

- tradeoffs,
- data architecture,
- reliability,
- replication,
- sharding,
- transactions,
- distributed systems,
- stream processing.

### Course mapping

```text
Week 1 → Chapters 1–2 (optional skim)
Week 2 → storage/data model chapters
Week 6 → dataflow / distributed processing
Week 9 → distributed-system failures + consistency
Week 10 → architecture tradeoffs
```

---

## Computer Networking: A Top-Down Approach, 9th Edition

**James F. Kurose & Keith Ross — Pearson, 2025/©2026**

https://www.pearson.com/en-us/subject-catalog/p/computer-networking-a-top-down-approach/P200000013385

Best for:

- application-layer networking,
- HTTP,
- DNS,
- transport,
- congestion,
- modern HTTP/3/QUIC context.

This is the best “I want networking depth without becoming a router firmware engineer” companion for this roadmap.

---

## Site Reliability Engineering

**Beyer, Jones, Petoff, Murphy (eds.) — Google/O'Reilly**

Read online:

https://sre.google/sre-book/table-of-contents/

Best for:

- reliability,
- SLOs,
- monitoring,
- load balancing,
- overload,
- cascading failures.

---

## The Site Reliability Workbook

Read online:

https://sre.google/workbook/table-of-contents/

Best for:

- turning SRE principles into exercises,
- SLO implementation,
- incident/reliability practice,
- non-abstract large system design.

---

## System Design Interview — An Insider's Guide, Vol. 1

**Alex Xu**

Useful for:

- estimation,
- design interview structure,
- classic systems,
- practicing communication.

Use it as **practice material**, not protocol documentation.

---

## System Design Interview — An Insider's Guide, Vol. 2

**Alex Xu & Sahn Lam**

Useful later for:

- bottlenecks,
- queues,
- metrics systems,
- object storage,
- payment systems.

---

# 7. Suggested Week 1 Reading Schedule

| Day | Required external reading | Optional |
|---|---|---|
| 1 | MDN HTTP overview + Google SRE golden signals | DDIA Ch. 1–2 |
| 2 | RFC 9110 selected sections + MDN methods/status | RFC 8446 intro |
| 3 | Cloudflare DNS + caching | MDN caching |
| 4 | RFC 9293 intro + MDN WebSocket | RFC 6455 / UDP |
| 5 | Google SRE load balancing | AWS/NGINX docs |
| 6 | Google SRE SLO + monitoring | System Design Interview Vol. 1 |
| 7 | No new reading | revisit weakest source |

---

# 8. How to Read Technical Sources

Do not highlight everything.

For each source, extract only:

```text
1. One definition
2. One diagram or mental model
3. One failure mode
4. One tradeoff
5. One question you still have
```

Then close the source and reconstruct it from memory.

That is far more useful than collecting 47 browser tabs like Pokémon.
