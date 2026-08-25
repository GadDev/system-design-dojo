# Week 1 Cheat Sheet

## Request path

```text
Browser → DNS → CDN/Edge → Load Balancer → API → Cache/Database
```

## Latency

Time required for one operation.

## Throughput

Amount of work completed per unit of time.

## HTTP

Request/response application protocol.

Useful codes:

```text
200 OK
201 Created
202 Accepted
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
429 Too Many Requests
500 Internal Server Error
502 Bad Gateway
503 Service Unavailable
504 Gateway Timeout
```

## Idempotency

Repeating an operation produces the same intended effect as performing it once.

Especially important when clients retry after uncertain network failures.

## HTTPS / TLS

Key properties:

```text
Confidentiality
Integrity
Server authentication
```

## DNS

Maps names to network destinations.

### TTL

Controls how long DNS information may be cached.

## CDN

Serves cacheable content nearer to users.

Think:

```text
latency ↓
origin load ↓
bandwidth pressure ↓
cache invalidation complexity ↑
```

## TCP

Reliable ordered byte stream with retransmission and congestion/flow control.

## UDP

Datagram transport with fewer built-in reliability guarantees.

## WebSockets

Long-lived bidirectional connection.

Good when genuine realtime server push is valuable.

## Polling

Repeated HTTP reads.

Simple, stateless, often perfectly adequate for background-job progress.

## Reverse proxy

Receives requests on behalf of backend services and can handle routing, TLS termination, compression, access control, and more.

## Load balancer

Distributes requests across backend instances.

## Stateless API

Does not rely on instance-local state surviving between requests.

This makes horizontal scaling and failover easier.

## Five questions to ask constantly

```text
What problem are we solving?
What is the bottleneck?
What happens when this component fails?
What happens at 10× traffic?
What tradeoff did we just introduce?
```

---

# Extended Cheat Sheet

## Latency percentiles

```text
p50 = median
p95 = 95% of observations are at or below this value
p99 = tail latency indicator
```

Watch tail latency under load.

## Golden signals

```text
Latency
Traffic
Errors
Saturation
```

## DNS records

```text
A      → IPv4
AAAA   → IPv6
CNAME  → alias
MX     → mail routing
TXT    → text/policy/verification
NS     → authoritative nameserver
```

## HTTP semantics

```text
safe        ≠ changes no implementation state at all
idempotent  = repeated intended effect is same as once
retryable   = application can safely attempt again under defined rules
```

## Async HTTP pattern

```text
POST /jobs
→ 202 Accepted
→ Location/status URL

GET /jobs/{id}
→ queued | processing | done | failed
```

## HTTP versions — mental model

```text
HTTP/1.1 → TCP
HTTP/2   → TCP + multiplexed HTTP streams
HTTP/3   → QUIC over UDP
```

## Cache questions

```text
What is the key?
How long is it fresh?
Can stale data be tolerated?
How is it invalidated?
What happens on cache failure?
What happens on mass cache miss?
```

## Realtime choices

```text
Polling     → simple repeated reads
SSE         → server → client event stream
WebSocket   → bidirectional persistent channel
WebTransport→ lower-level advanced realtime transport
```

## Load balancing

```text
L4-ish → network/connection information
L7     → application protocol information
```

## Health

```text
Liveness  → should this process be restarted?
Readiness → should this instance receive new traffic?
```

## Statelessness

```text
Instance-local hidden state should not be required
for another instance to correctly handle the next request.
```

It does **not** mean the system has no state.

## Scaling rule

Before adding technology:

```text
1. Define target.
2. Measure current behavior.
3. Find saturation/bottleneck.
4. Make one justified change.
5. Measure again.
```

## Decision sentence

Use:

> Because **[requirement/evidence]**, I choose **[decision]**, accepting **[tradeoff]**. I would reconsider if **[trigger]**.

Example:

> Because profile reads are highly repetitive and DB read saturation pushes p95 above our target, I would add a cache-aside layer, accepting bounded staleness and cache-failure complexity. I would reconsider the design if hit ratio stays low.
