# Week 4 Cheat Sheet — Horizontal Scaling

## Vertical scaling

```text
bigger machine
```

Useful when simplicity wins and a single node can still meet requirements.

## Horizontal scaling

```text
more instances
```

Requires traffic distribution and shared/externalized important state.

---

# Stateless API

```text
Any healthy instance can serve the next request.
```

Important state is not trapped only in instance-local memory.

---

# Load balancer

```text
Client → LB → API replicas
```

Common algorithms:

```text
round robin
least connections
weighted
hash/affinity
```

---

# Liveness vs readiness

```text
Liveness  → should process be restarted?
Readiness → should new traffic be sent here?
```

During shutdown:

```text
unready → drain → terminate
```

---

# Sticky sessions

```text
same client → same backend
```

Tradeoffs:

```text
locality ↑
flexibility ↓
failover complexity ↑
load skew risk ↑
```

---

# Autoscaling

```text
measure → compare → scale → warm up → ready
```

Signals:

```text
CPU
memory
RPS
concurrency
queue depth
custom metrics
```

Remember:

```text
autoscaling has delay
```

Therefore maintain:

```text
headroom + overload protection
```

---

# DB connection multiplier

```text
replicas × pool size = possible DB connections
```

Always model this before raising max replicas.

---

# Rate limiting

## Fixed window

Simple, boundary bursts possible.

## Sliding window

More accurate rolling interval.

## Token bucket

```text
bucket size → burst allowance
refill rate → sustained rate
```

## Leaky bucket

Smooth outgoing rate.

---

# 429

```http
429 Too Many Requests
Retry-After: 30
```

Use when a client/identity exceeds an applicable rate policy.

---

# Rate vs quota vs concurrency

```text
Rate        → operations / time
Quota       → total entitlement
Concurrency → simultaneous work
```

---

# Backpressure

```text
downstream full
→ upstream slows/waits within bound/rejects
```

---

# Admission control

```text
Should we accept this new work?
```

Possible:

```text
accept
bounded wait
reject temporary
reject permanent
```

---

# Load shedding

Reject/degrade some traffic to preserve useful throughput during overload.

Possible response:

```http
503 Service Unavailable
Retry-After: 10
```

---

# Retry rule

```text
retries are traffic
```

Use:

```text
idempotency
bounded attempts
exponential backoff
jitter
deadlines
```

---

# Upload architecture

Bad for GB-scale media:

```text
Client → API → Object Storage
```

Preferred:

```text
CONTROL:
Client → LB → FastAPI → DB/Redis

DATA:
Client =================> Object Storage
```

---

# 10,000 uploads mental math

Assume:

```text
10k × 1 GB = ~10 TB media
```

15-minute uniform transfer:

```text
~89 Gbit/s aggregate
```

If 10k init calls arrive in one minute:

```text
~167 RPS average
```

Separate **bytes** from **control requests**.

---

# Seven scaling questions

```text
1. What is saturated?
2. Which metric proves it?
3. Does adding replicas increase that capacity?
4. What becomes the next shared bottleneck?
5. How long does capacity take to arrive?
6. What protects us while waiting?
7. What does the user experience under overload?
```
