# Week 12 — Final Review Notes

Do the defense first.

## Numeric anchors

34. `100,000 × 60 = 6,000,000` one-minute chunks/day.
35. `6,000,000 ÷ 86,400 ≈ 69.4 chunks/sec` average.
36. `69.4 × 15 ≈ 1,041` average concurrent chunk executions before headroom/peaks.

## Selected conceptual answers

1. So large bytes do not consume/scalably couple API compute/network capacity; API manages authorization/session/control while storage carries media.
5. Repeated delivery of large mostly immutable objects to globally distributed consumers.
13. Ordinary accounts can precompute timelines cheaply enough; celebrity fan-out creates extreme write amplification, so merge their posts on read.
19. Location can be approximate/fresh-enough, but assigning one driver to two riders violates a core business invariant.
22. They have different mutation, consistency, durability and scaling patterns.
25. Multiple clients can independently progress while unable to coordinate, then must reconcile on reconnection.
29. Streaming scale is often dominated by Tbps-scale bytes, while metadata API RPS can be comparatively modest.
37. It makes expensive output discoverable/reusable after ambiguous failure and helps idempotent reconciliation.
38. The broker knows whether a message is pending/acked; it does not necessarily know whether the business state/artifact was durably accepted.
40. Queue age/backlog relative to completion throughput, constrained by provider/GPU quotas; not blindly API CPU.
41. Per-tenant concurrency/quotas/fair scheduling.
44. Examples: durable replay by multiple independent consumers, long-lived event history, partitioned stream processing or very high event throughput that exceeds simpler broker needs.
45. Complex long-running workflows, many durable timers/signals/branches, high operational pain from custom orchestration/recovery.
47. Legal basis/processor relationships, minimization, retention, user rights, security, residency/transfers, purpose limitation and auditable deletion — not residency alone.
48. Verify authoritative state, artifact/result integrity, user-visible progress, queue/DLQ state and relevant SLO/metrics return to normal.
49. A measurable workload/organizational requirement such as replica lag, QPS, team ownership, retry complexity, or queue retention/replay need — not a vague “when we scale.”
50. Start from requirements, quantify magnitude, choose the smallest architecture that meets them, make failure/data authority explicit, and defend tradeoffs with revisit triggers.
