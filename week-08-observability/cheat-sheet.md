# Week 8 — Observability Cheat Sheet 🥋

## Three core signals

```text
Logs    → discrete events / details
Metrics → aggregates / trends / alertable numbers
Traces  → causal path + timing across components
```

## Correlation scopes

```text
request_id → HTTP request
trace_id   → distributed causal execution
job_id     → business workflow
chunk_id   → child unit
message_id → queue delivery/event
```

## Structured log fields

```text
timestamp
level
service
event
job_id
chunk_index
worker_id
attempt
error_class
trace_id
duration_ms
```

Never casually log:

```text
transcript text
tokens/secrets
presigned URLs
email/PII
raw media
```

## Prometheus metric types

```text
Counter   → only increases
Gauge     → up/down current value
Histogram → distribution of observations
```

## Cardinality

```text
status/provider/queue → often bounded labels
job_id/user_id/email  → usually NOT metric labels
```

## API RED

```text
Rate
Errors
Duration
```

## Worker/pipeline essentials

```text
queue_depth
oldest_queued_job_age
arrival_rate
completion_rate
worker_utilization
retry_rate
chunk_duration p95/p99
DLQ growth
```

## Trace

```text
Trace = distributed operation
Span  = one operation within trace
```

Propagate context across:

```text
HTTP
queue messages
worker boundaries
```

## OpenTelemetry

```text
instrumentation
   ↓
API / SDK
   ↓
exporter
   ↓
Collector
   ↓
backend(s)
```

## Reliability language

```text
SLI → measurement
SLO → target
SLA → external agreement
Error budget → allowed unreliability
```

## Stuck-job investigation

```text
1. authoritative DB state
2. determine stuck stage
3. system-wide metrics
4. job logs
5. distributed trace
6. incident timeline
7. recovery
8. user communication
9. telemetry improvement
```

## Golden question

```text
Is this one bad job,
or is the system unhealthy?
```
