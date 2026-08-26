# Local Observability Stack

This is a teaching stack, not a production blueprint.

```text
FastAPI
  ├── JSON logs → stdout
  ├── Prometheus metrics → /metrics
  └── OTel traces → Collector → Tempo

Prometheus ─┐
Tempo ──────┼→ Grafana
```

## Run

```bash
docker compose up --build
```

Generate traffic:

```bash
for i in {1..20}; do
  curl -s -X POST http://localhost:8000/jobs
  echo
done
```

Inspect:

```text
http://localhost:9090      Prometheus
http://localhost:3000      Grafana
http://localhost:8000/docs FastAPI
```

Grafana local credentials:

```text
admin / admin
```

## PromQL ideas

```promql
sum(rate(demo_http_requests_total[1m]))
```

```promql
histogram_quantile(
  0.95,
  sum by (le) (rate(demo_http_request_duration_seconds_bucket[5m]))
)
```

```promql
demo_transcription_queue_depth
```

## Trace exercise

Create a job, copy the `trace_id` from the structured application log, then find the trace in Tempo through Grafana.

Ask:

```text
Which service created the trace?
Which span attributes are business-level vs framework-level?
What information would you add for a real queue/worker path?
```

## Caveat

Container image versions are intentionally left as `latest` for a short-lived educational lab. Pin versions in a real repository once you choose a tested stack.
