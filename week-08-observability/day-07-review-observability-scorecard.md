# Day 7 — Observability Review & Incident Defense 🥋

## Goal

Prove you can diagnose distributed-system behavior without relying on memorized dashboards.

---

# Part 1 — Blank-page observability architecture

Without notes, draw:

```text
FastAPI
Queue
Worker
PostgreSQL
R2
AI Provider
```

Add:

```text
logs
metrics
traces
OpenTelemetry
Prometheus
Grafana
```

Explain the role of each.

---

# Part 2 — 40-question retrieval review

Use `review-and-quiz.md`.

Do not open the answer key until you have committed your answers.

---

# Part 3 — 90-second oral defenses

Explain each aloud:

1. Logs vs metrics vs traces.
2. Why `job_id` belongs in logs but normally not Prometheus labels.
3. Why queue depth alone is insufficient.
4. How trace context crosses a queue boundary.
5. SLI vs SLO vs SLA.
6. Why alerts should prefer user symptoms.
7. How you investigate a stuck job.

If you use a technology name, state **what problem it solves**.

---

# Part 4 — Observability scorecard

Score each 0–2:

```text
0 = absent
1 = partial/inconsistent
2 = intentional and usable
```

| Capability | Score |
|---|---:|
| Structured JSON logs | |
| Stable event taxonomy | |
| Job/chunk correlation | |
| Trace IDs in logs | |
| Sensitive-data policy | |
| API RED metrics | |
| Queue age/depth metrics | |
| Worker throughput/utilization | |
| Dependency metrics | |
| Histogram-based latency | |
| Cardinality controls | |
| End-to-end tracing | |
| Queue context propagation | |
| Sampling policy | |
| Product SLIs | |
| Documented SLOs | |
| Error-budget thinking | |
| Product-health dashboard | |
| Actionable alerts | |
| Runbooks | |
| Incident timeline template | |
| Telemetry retention/cost policy | |

Maximum: **44**.

The number is less important than the gaps you can explain.

---

# Part 5 — Incident defense

Prompt:

> Job `abc123` has shown 68% progress for 30 minutes.

You have 10 minutes to present:

```text
1. first query/check
2. metrics you inspect
3. logs you query
4. trace you follow
5. likely failure classes
6. recovery decision
7. user-facing status
8. alert/dashboard improvement after incident
```

Do not start with:

> “I would restart everything.”

That's not observability. That's interpretive dance. 😄

---

# Week 8 final deliverable

Create:

```text
my-observability-review.md
```

containing:

1. telemetry architecture diagram,
2. logging contract,
3. metric catalog,
4. trace design,
5. 3–5 SLOs,
6. dashboard layout,
7. alert/runbook examples,
8. stuck-job investigation flow,
9. telemetry privacy/cost rules,
10. three gaps you would fix before production.

## Exit criterion

You can answer **“why is job 123 stuck?”** using evidence from the appropriate signals and communicate both immediate recovery and the missing observability that allowed the issue to remain confusing.
