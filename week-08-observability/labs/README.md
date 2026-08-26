# Week 8 Labs 🔬

## Lab A — Stuck-job investigation

Files:

```text
sample-events.jsonl
stuck_job_investigator.py
```

Run:

```bash
python stuck_job_investigator.py sample-events.jsonl job_abc123
```

Before running the script, inspect the JSONL manually and form a hypothesis.

---

## Lab B — Metrics/traces instrumentation sketch

`observability-stack/` contains a small reference stack:

```text
FastAPI app
  ├── structured JSON logs
  ├── /metrics for Prometheus
  └── OpenTelemetry traces → Collector → Tempo

Prometheus ─┐
Tempo ──────┼→ Grafana
```

This lab is meant to teach component boundaries rather than production deployment.

Run where Docker Compose is available:

```bash
cd observability-stack
docker compose up --build
```

Then:

```text
FastAPI:    http://localhost:8000
Prometheus: http://localhost:9090
Grafana:    http://localhost:3000
Tempo:      http://localhost:3200
```

Grafana default local credentials in this lab:

```text
admin / admin
```

Do not reuse those credentials anywhere real.

---

## Lab C — Alert rules

Inspect:

```text
observability-stack/alerts.yml
```

For every rule explain:

```text
what user symptom it approximates
why the threshold/window exists
which runbook action should follow
how it could false-positive
```
