# Week 7 — Answer Key

Use only after attempting the review.

1. Slow responses hold scarce capacity and can cause queues/pools to saturate even without explicit errors.
2. Timeout bounds one operation; deadline is the latest acceptable completion time for a larger operation.
3. Connection timeout bounds establishment; request/read timeout bounds waiting for operation/response.
4. It creates false failures and unnecessary retry traffic.
5. It pins resources and delays failure handling.
6. The remote operation may have completed while its response was lost/delayed.
7. Measured downstream latency distributions, workload semantics, end-to-end deadline, network and retry policy.
8. Otherwise retries silently violate the total operation latency/recovery objective.
9. Selected network failures, transient 5xx, documented 429/rate limit with retry guidance.
10. Validation errors, auth/permission failures, unsupported/corrupt deterministic input.
11. Extra attempts add load precisely when the dependency may already be overloaded.
12. Wait grows exponentially between attempts, usually with a cap.
13. Prevents absurdly long waits and keeps recovery bounded.
14. Spreads correlated retry attempts over time.
15. Attempts multiply across layers.
16. Ambiguous outcomes can cause the same logical mutation to execute more than once.
17. Calls pass while outcomes are measured.
18. Calls fail/short-circuit without contacting dependency.
19. Limited probes test whether dependency recovered.
20. Prevents one/few failures from producing unstable breaker decisions.
21. Latency can exhaust capacity before hard errors appear.
22. Timeout bounds waiting; breaker decides whether to call at all based on health history.
23. Breaker reacts to dependency health; limiter controls permitted traffic rate/amount.
24. Isolation/concurrency boundary preventing one workload/dependency from consuming all capacity.
25. Continue useful safe behavior with reduced functionality.
26. Hard dependency is required for correctness of an operation; soft dependency can be unavailable while operation still provides valid reduced behavior.
27. Has application finished starting?
28. Is the process in a state where restart is likely to help?
29. Should this instance receive traffic now?
30. DB outage could cause all pods to restart together and amplify the outage/connection storm.
31. Allows load balancer/service routing to drain new traffic before process exits.
32. Transcript available while summary/search/analytics is delayed; or uploads accepted while provider processing is paused if durable intake remains healthy.
33. Target maximum recovery duration.
34. Target maximum acceptable data-loss window.
35. Recent acknowledged data may not yet have reached a replica at primary failure.
36. Multiple nodes believe they are authoritative primary and accept conflicting writes.
37. A successful promotion can leave the system with no redundant standby and therefore still degraded.
38. Providers may differ in quality, timestamps, languages, cost, compliance and output semantics.
39. Use deterministic identity/artifact, idempotent/guarded persistence, reconcile existing durable effects, then ACK.
40. Successful controlled probes plus stable latency/error/capacity metrics over a defined recovery window, not merely one successful request.

---

## Strong Week 7 design checklist

```text
bounded waits
explicit retry classes
idempotent retryable effects
capped exponential backoff + jitter
one intentional retry layer
circuit breaker where useful
bulkhead/concurrency isolation
degraded-mode behavior
correct startup/liveness/readiness semantics
graceful draining
RTO/RPO for stateful data
failover with old-primary fencing
DLQ with owner/redrive
recovery verified by evidence
```
