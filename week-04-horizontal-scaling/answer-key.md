# Week 4 — Answer Key

Use only after attempting the quiz.

---

# 1–8 Scaling fundamentals

1. **Vertical scaling:** increase resources of an existing node/instance, such as CPU or memory.
2. **Horizontal scaling:** add more independently serving instances/nodes.
3. Vertical can be preferable when workload is modest, one larger node solves the problem, and operational simplicity matters.
4. Horizontal is valuable for elastic traffic, aggregate capacity, rolling deployment, and instance-failure tolerance.
5. More API replicas can open more DB connections and generate more concurrent queries.
6. A stateless API does not depend on one particular instance retaining cross-request state required for correctness.
7. No. State lives in shared/durable systems or travels with requests.
8. Workers may be multiple processes on one machine/failure domain; replicas are independent service instances, potentially across machines.

---

# 9–18 Load balancing

9. Distribute incoming work/connections across available serving instances.
10. L4 routes primarily using transport/network information; L7 understands application protocol such as HTTP and can route by host/path/header.
11. Round robin rotates requests across backends.
12. Least connections prefers a backend with fewer active connections.
13. Weighted balancing fits mixed-capacity fleets or controlled rollout.
14. Skewed keys/clients can concentrate traffic, and affinity reduces redistribution freedom.
15. Liveness asks whether process should be restarted; readiness asks whether it should receive new traffic.
16. To stop new work while allowing in-flight work to finish within a deadline.
17. Routing that tries to keep the same client/session on the same backend.
18. Uneven load, harder failover, coupling to instance lifetime, rollout/draining complexity.

---

# 19–28 Autoscaling

19. It periodically observes metrics, decides, changes replica count, then waits for new capacity to become useful.
20. Metric collection, decision interval, scheduling/provisioning, image/container startup, app warmup, readiness.
21. The service may spend most time waiting on DB/network while CPU remains low.
22. When request cost is reasonably stable and tested per-replica RPS correlates with saturation.
23. It measures in-flight work and can fit I/O-heavy services where CPU is not the dominant resource.
24. Warm capacity absorbs bursts/failover and avoids scale-from-zero delay.
25. Cost control and protection of shared dependencies such as DB connections/downstream quotas.
26. Repeated scale up/down caused by noisy/oscillating signals and insufficient stabilization.
27. Not-ready instances should not be treated as useful serving capacity; startup spikes can also distort metrics.
28. Capacity takes time to arrive and sudden bursts can exceed current capacity immediately.

---

# 29–40 Rate limiting and overload

29. Rate = operations/time; quota = total allowance; concurrency = simultaneous active work.
30. Requests can cluster just before and after a window boundary, creating a burst larger than the intended smooth rate.
31. Allowed burst size.
32. Sustainable long-run arrival allowance.
33. Requests can land on different replicas, each with an independent counter, multiplying the total allowance.
34. The client has sent too many requests for an applicable rate policy.
35. Mechanism by which upstream slows/pauses/rejects because downstream capacity is constrained.
36. Decision whether to accept new work at all.
37. Deliberately reject/degrade some work to preserve useful throughput under overload.
38. Unbounded queues turn overload into unbounded latency/memory/backlog and may process stale work.
39. Timeouts create retries, retries add traffic, extra traffic creates more timeouts—a positive feedback loop.
40. Jitter prevents many clients from retrying in synchronized waves.

---

# Scenario guidance

## A

Do **not** blindly scale APIs. PostgreSQL/connection capacity is already the constraint; more replicas may amplify it. Investigate pooling, query latency, connection budget, and request concurrency.

## B

If load tests show useful throughput increases with more replicas and shared dependencies remain healthy, high CPU plus rising latency supports horizontal API scaling.

## C

Warm headroom, rate limiting, admission control, bounded concurrency/queues, graceful degradation/load shedding.

## D

In the worst simple interpretation, up to ~2,000 requests/min if the user's requests are distributed across all 20 independent local limits.

## E

503 → immediate retries → more traffic → more overload → more 503/timeouts → more retries.

## F

Bandwidth, long-lived connections/sockets, buffers/memory, TLS/proxy CPU, file descriptors, timeouts, and potentially egress toward object storage.
