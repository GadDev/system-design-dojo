# Transcription Observability Dashboard Plan

## Dashboard 1 — Product Health

| Question | Suggested signal |
|---|---|
| Can users create jobs? | job-acceptance success ratio |
| Are jobs starting on time? | time-to-start p50/p95/p99 |
| Are jobs completing? | completion success ratio |
| Are jobs getting stuck? | progress freshness / stuck-job count |
| How long are jobs taking? | processing-duration / media-duration distribution |

## Dashboard 2 — Pipeline

| Question | Suggested signal |
|---|---|
| Is work arriving faster than it completes? | arrival rate vs completion rate |
| Is backlog growing? | queue depth + oldest queued age |
| Are workers saturated? | busy/total workers |
| Are chunks slowing down? | chunk duration p50/p95/p99 |
| Are retries increasing? | retry rate by bounded error class |
| Is unrecoverable work accumulating? | DLQ size/growth |

## Dashboard 3 — Dependencies

| Dependency | Signals |
|---|---|
| PostgreSQL | query latency, errors, pool saturation |
| Redis/queue | operation latency, failures, pending/backlog |
| R2 | request latency, 4xx/5xx by operation |
| AI provider | latency, 429 rate, 5xx rate, timeout rate |

## Navigation design

```text
Product symptom
   ↓
Pipeline stage
   ↓
Dependency
   ↓
Trace exemplar
   ↓
Job/chunk logs
```

Every panel should have an answer to:

> If this looks bad, where do I click or query next?
