# Day 5 — Grafana Dashboards, Alerting & Signal Correlation

## Goal

Build views and alerts that help an engineer **decide what to do next**.

---

## 1. Dashboard hierarchy

Do not create one 97-panel dashboard.

Use layers.

### Level 1 — Product health

```text
job acceptance rate
completion success
processing latency
oldest queued job
stuck-job count
```

### Level 2 — Pipeline health

```text
queue depth
arrival rate
completion rate
retry rate
worker utilization
chunk p95/p99 duration
```

### Level 3 — Dependency health

```text
PostgreSQL latency / pool pressure
Redis errors / latency
R2 error rate
AI provider latency / 429 / 5xx
```

The first screen tells you **whether users are hurting**. The next screens help explain why.

---

## 2. Prometheus + Grafana mental model

```text
Application / exporter
        ↓
   Prometheus scrape
        ↓
 Prometheus TSDB
        ↓
      PromQL
        ↓
      Grafana
```

Grafana is the visualization/alerting interface; Prometheus is the metrics collection/query system in this architecture.

---

## 3. A dashboard should answer questions

Good panel:

```text
Are jobs entering faster than they complete?
```

Show together:

```text
accepted jobs/sec
completed jobs/sec
queue depth
oldest queued age
```

Bad panel:

```text
worker_7_cpu_temperature
```

unless that metric answers a real operational question.

---

## 4. Alert on symptoms when possible

Weak alert:

```text
CPU > 80%
```

Stronger user-impact alert:

```text
p95 time-to-start > SLO
AND
oldest queued job > threshold
```

Dependency alerts are still useful, but paging should prioritize actionable user impact.

---

## 5. Actionable alerts

An alert should include:

```text
What is wrong?
Who/what is affected?
How bad is it?
How long has it been happening?
Which dashboard/query should I inspect?
Which runbook applies?
```

Example:

```yaml
summary: "Transcription queue delay above SLO"
description: "Oldest queued job > 10m for 15m"
runbook: "runbooks/transcription-queue-delay.md"
```

If the recipient has no plausible action, ask whether it should be a page, ticket or dashboard signal instead.

---

## 6. Avoid alert fatigue

Bad:

```text
AI call failed once → page
```

Better:

```text
provider failure/rate-limit rate exceeds sustained threshold
AND/OR
user-facing SLO is burning rapidly
```

Expected transient recovery should not wake a human every time it works.

---

## 7. Metrics → traces → logs

A powerful investigation flow is:

```text
Grafana metric spike
      ↓
exemplar / trace link
      ↓
slow/error trace
      ↓
trace_id in logs
      ↓
job-specific events
```

Exemplars act like bookmarks from aggregate metric observations to representative traces.

---

## 8. Suggested dashboards

### Dashboard A — Service Overview

```text
Job acceptance success
Job completion success
p50/p95/p99 completion ratio
Oldest queued job
Stuck processing jobs
```

### Dashboard B — Worker Pipeline

```text
Queue depth
Arrival vs completion rate
Busy/total workers
Chunk duration histogram
Retry rate
DLQ growth
```

### Dashboard C — Dependencies

```text
DB query latency
DB pool saturation
Redis latency/errors
R2 error rate
AI latency
AI 429/5xx
```

---

## Exercise — Design the “stuck jobs” dashboard

Your dashboard must answer within 60 seconds:

```text
Is this one job or systemic?
Which stage is accumulating work?
Are workers saturated?
Is a dependency throttling/failing?
When did the problem begin?
```

For every panel specify:

```text
question
metric/query
visualization
threshold/context
next action
```

---

## Break it 💥

You have 80 dashboards and 430 alerts.

The team ignores half the notifications.

Explain why **more observability data** can produce **less operational understanding**.

---

## Retrieval quiz

1. What should Level 1 dashboards emphasize?
2. Why prefer symptom alerts for paging?
3. What makes an alert actionable?
4. What is alert fatigue?
5. How can exemplars help investigation?
6. Why put arrival rate and completion rate beside queue depth?

## Exit criterion

You can design a small dashboard/alert set that helps an on-call engineer move from symptom to likely dependency without opening dozens of unrelated panels.
