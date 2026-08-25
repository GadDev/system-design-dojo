# Week 4 — Review & 40-Question Retrieval Quiz

## Goal

Prove that you can reason about capacity and overload without reaching for buzzwords.

Answer without notes first.

---

# Part 1 — Scaling fundamentals

1. Define vertical scaling.
2. Define horizontal scaling.
3. Give one case where vertical scaling may be preferable.
4. Give one case where horizontal scaling is valuable.
5. Why can adding API replicas make PostgreSQL worse?
6. What does “stateless API” mean?
7. Does stateless mean no state exists anywhere?
8. Difference between multiple FastAPI workers and multiple service replicas?

---

# Part 2 — Load balancing

9. What problem does a load balancer solve?
10. Difference between L4- and L7-style balancing?
11. Explain round robin.
12. Explain least connections.
13. When is weighted balancing useful?
14. Why can hash-based affinity create uneven load?
15. Difference between liveness and readiness?
16. Why drain connections before terminating an instance?
17. What is a sticky session?
18. Name two costs of sticky sessions.

---

# Part 3 — Autoscaling

19. Why is autoscaling a delayed control loop?
20. Name four scale-up delays.
21. Why can CPU be a poor signal for an I/O-bound API?
22. When can RPS be a useful scaling signal?
23. Why can concurrency be useful?
24. Why set minimum replicas?
25. Why set maximum replicas?
26. What is autoscaling thrash?
27. How can readiness affect autoscaling accuracy?
28. Why doesn't autoscaling remove the need for headroom?

---

# Part 4 — Rate limiting and overload

29. Difference between rate limit, quota, and concurrency limit?
30. What is the boundary-burst problem in a fixed window?
31. What does token-bucket capacity represent?
32. What does token-bucket refill rate represent?
33. Why can per-instance local rate limits fail to enforce one global user limit?
34. What does HTTP 429 mean?
35. Define backpressure.
36. Define admission control.
37. Define load shedding.
38. Why should queues be bounded?
39. Why can retries cause cascading failures?
40. Why use jitter with exponential backoff?

---

# Part 5 — Architecture debugging

## Scenario A

```text
API CPU = 22%
DB pool wait p95 = 900ms
PostgreSQL connections = 98% budget
```

Should you scale APIs up? Explain.

## Scenario B

```text
API CPU = 90%
p95 rising
DB healthy
```

What evidence would support horizontal API scaling?

## Scenario C

HPA can add replicas in 60 seconds but traffic doubles in 3 seconds.

What protects the service during the gap?

## Scenario D

Each of 20 replicas allows a local limit of 100 requests/min/user.

What could the effective global limit become?

## Scenario E

Clients retry every 503 immediately.

Explain the feedback loop.

## Scenario F

A 2 GB upload passes through FastAPI before reaching R2.

Name at least four resources the API tier now spends on the media transfer.

---

# Part 6 — Blank-page design

Without looking at Week 4 files, draw:

```text
Client
 ↓
LB
 ├─ API
 ├─ API
 └─ API
 ↓
Redis + PostgreSQL
```

Then add:

- readiness,
- rate limiting,
- autoscaling signal,
- direct object-storage upload,
- overload rejection point.

Explain each addition in one sentence.

---

# Part 7 — Oral defense

Give yourself 2 minutes each.

### Prompt A

> Why is statelessness useful for horizontal scaling?

### Prompt B

> When would sticky sessions be justified?

### Prompt C

> Why can autoscaling make a database outage worse?

### Prompt D

> Rate limiting vs backpressure vs load shedding?

### Prompt E

> Design the upload path for 10,000 simultaneous 1 GB videos.

---

# Score yourself

For the 40 direct questions:

| Score | Meaning |
|---|---|
| 36–40 | Strong — proceed |
| 31–35 | Good — review 1–2 weak areas |
| 24–30 | Revisit at least two lessons |
| <24 | Repeat the core lessons before Week 5 |

Do not count a memorized definition as mastery if you cannot apply it to the scenarios.
