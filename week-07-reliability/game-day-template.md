# Reliability Game-Day Template

## Experiment name

```text
Example: Worker dies after durable output but before broker ACK
```

## Hypothesis

State the behavior you believe the system guarantees.

> If ___ fails while ___, then ___ will happen within ___ without violating ___ invariant.

## Preconditions

- environment:
- traffic level:
- test data:
- required dashboards/logs:
- backups/recovery verified:

## Blast radius

```text
Which users/jobs/components can be affected?
Maximum acceptable scope?
```

## Fault injection

Describe exactly what is being changed or killed.

## Expected behavior

```text
Detection:
Immediate reaction:
Retry/degrade/failover:
User-visible behavior:
Recovery:
```

## Metrics to watch

- latency:
- error rate:
- saturation:
- retry amplification:
- queue age/depth:
- breaker state:
- failover/recovery time:
- correctness invariant:

## Abort conditions

Stop immediately if:

- data integrity is threatened,
- blast radius exceeds agreed scope,
- recovery path behaves unexpectedly,
- safety/operational owner requests stop.

## Recovery procedure

1. Restore normal dependency behavior.
2. Verify traffic/retry rate stabilizes.
3. Reconcile durable state.
4. Redrive only safe failed work.
5. Confirm correctness invariants.
6. Restore full traffic gradually.

## Evidence

```text
What observations prove the hypothesis?
What surprised us?
What failed differently from expectation?
```

## Follow-up actions

| Action | Owner | Priority | Verification |
|---|---|---|---|
| | | | |
