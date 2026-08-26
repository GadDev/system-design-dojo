# Failure Matrix Template

Use one row per meaningful failure mode. Split a dependency into multiple rows when failure semantics differ (for example, `429` vs `401` vs timeout).

| Component | Operation | Failure mode | Detection | Timeout | Retry? | Idempotency | Breaker/Bulkhead | Degraded behavior | Failover | RTO/RPO | User impact | Recovery proof |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | |

## Review questions

For each row, answer:

1. Is the failure transient, permanent, ambiguous, slow, or overload-related?
2. What durable state may already have changed before the failure became visible?
3. Could a retry duplicate a side effect?
4. What prevents synchronized retry traffic?
5. What is the terminal state after automated recovery is exhausted?
6. Is there a safe reduced-functionality mode?
7. If failover occurs, what prevents two primaries/owners from acting simultaneously?
8. What measurable evidence proves normal traffic can resume?
