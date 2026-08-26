# Day 2 — Metrics, Prometheus & Cardinality

## Goal

Use metrics to answer **how much, how often, how slow and how unhealthy** without querying millions of individual log events.

---

## 1. Metrics are aggregates

Logs tell you:

```text
chunk 42 retried at 08:14
```

Metrics tell you:

```text
retry rate increased from 0.8% to 17% across the worker fleet
```

That difference matters.

---

## 2. Core Prometheus metric types

### Counter

Only increases (except reset on restart).

```text
transcription_chunk_attempts_total
transcription_provider_errors_total
transcription_jobs_completed_total
```

Use `rate()` to reason about change over time.

### Gauge

Can increase and decrease.

```text
transcription_queue_depth
transcription_workers_busy
transcription_jobs_processing
```

### Histogram

Records a distribution of observations.

```text
transcription_chunk_processing_duration_seconds
http_request_duration_seconds
```

Histograms are useful when averages hide the tail.

---

## 3. Metrics for this pipeline

A useful first catalog:

```text
# API
http_requests_total{route,method,status_class}
http_request_duration_seconds{route,method}

# Queue
transcription_queue_depth{queue}
transcription_oldest_queued_job_age_seconds{queue}

# Workers
transcription_workers_busy{pool}
transcription_chunk_attempts_total{outcome,error_class}
transcription_chunk_processing_duration_seconds{model}
transcription_retries_total{reason}

# Workflow
transcription_jobs_total{status}
transcription_jobs_in_progress
transcription_job_completion_duration_seconds

# Dependencies
ai_requests_total{provider,outcome}
ai_request_duration_seconds{provider}
r2_requests_total{operation,outcome}
db_pool_in_use_connections
```

Keep dimensions bounded.

---

## 4. Cardinality: the expensive trap

Do **not** do this:

```text
transcription_job_status{job_id="abc123",user_id="xyz"} 1
```

If you have millions of jobs, you create millions of time series.

Prometheus labels should usually use bounded dimensions such as:

```text
status="failed"
provider="provider_a"
queue="transcription"
error_class="rate_limited"
```

Use logs/traces/database queries for individual `job_id` investigation.

Rule of thumb:

```text
bounded category → metric label candidate
unbounded identifier → usually logs/traces, not metric label
```

---

## 5. RED and worker-oriented signals

For synchronous APIs, think RED:

```text
Rate
Errors
Duration
```

For workers, also care about:

```text
queue depth
oldest job age
processing rate
failure/retry rate
worker utilization
processing-duration distribution
```

A queue depth of 5,000 means little without arrival/processing rates and job age.

---

## 6. Tail latency

Suppose durations are:

```text
99 jobs → 20 seconds
1 job   → 15 minutes
```

Average latency can look acceptable while one customer is miserable.

Track distributions and percentiles such as:

```text
p50
p95
p99
```

Example PromQL for a classic histogram:

```promql
histogram_quantile(
  0.95,
  sum by (le) (
    rate(transcription_chunk_processing_duration_seconds_bucket[5m])
  )
)
```

---

## 7. Useful PromQL exercises

### Worker failure rate

```promql
sum(rate(transcription_chunk_attempts_total{outcome="failed"}[5m]))
/
sum(rate(transcription_chunk_attempts_total[5m]))
```

### Queue backlog

```promql
transcription_queue_depth{queue="chunks"}
```

### Busy-worker ratio

If you export busy and total workers:

```promql
sum(transcription_workers_busy)
/
sum(transcription_workers_total)
```

### Provider 429 rate

```promql
sum(rate(ai_requests_total{outcome="rate_limited"}[5m]))
```

---

## 8. Metrics should answer decisions

Bad dashboard question:

> How many colorful graphs can we fit on screen?

Better:

> Is work entering faster than we can process it?

Then choose:

```text
arrival rate
completion rate
queue depth
oldest queued age
```

---

## Exercise — Metric catalog

For each item choose **counter / gauge / histogram** and labels:

1. jobs accepted,
2. active workers,
3. chunk duration,
4. AI 429s,
5. queue depth,
6. retries,
7. bytes uploaded,
8. time from upload-complete to job-start,
9. completed jobs,
10. PostgreSQL pool usage.

Then identify any labels that would create dangerous cardinality.

---

## Break it 💥

Your team proposes:

```text
chunk_duration_seconds{
  job_id,
  user_id,
  filename,
  chunk_id,
  worker_id
}
```

Explain why this is operationally dangerous and redesign it.

---

## Retrieval quiz

1. Counter vs gauge?
2. Why use a histogram for latency?
3. Why is average latency often insufficient?
4. Why should `job_id` not normally be a Prometheus label?
5. What does queue depth fail to tell you by itself?
6. What three signals does RED represent?

## Exit criterion

You can design a small metric catalog that detects queue buildup, worker saturation, provider failures and slow processing **without exploding cardinality**.
