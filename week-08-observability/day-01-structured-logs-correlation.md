# Day 1 — Structured Logs & Correlation

## Goal

Turn logs from prose written for humans into **queryable events** that let you reconstruct one job across many processes.

---

## 1. Logs answer event-level questions

A useful log is not:

```text
Something went wrong processing video
```

A useful structured event looks closer to:

```json
{
  "timestamp": "2026-08-26T08:14:03.451Z",
  "level": "warning",
  "service": "transcription-worker",
  "event": "chunk.retry_scheduled",
  "job_id": "job_abc123",
  "chunk_index": 42,
  "worker_id": "worker-7",
  "attempt": 2,
  "error_class": "provider_rate_limited",
  "retry_in_ms": 4187,
  "trace_id": "..."
}
```

The message is useful. The stable fields are what make investigation fast.

---

## 2. Build a logging schema

Recommended common fields:

| Field | Why it exists |
|---|---|
| `timestamp` | order events |
| `level` | severity |
| `service` | emitting component |
| `environment` | prod/staging/local |
| `event` | stable machine-queryable event name |
| `job_id` | correlate one transcription |
| `upload_id` | connect upload → job |
| `chunk_index` | identify child unit |
| `worker_id` | locate executor |
| `attempt` | retry history |
| `trace_id` | jump to distributed trace |
| `duration_ms` | operation timing when relevant |
| `error_class` | normalized failure category |

Keep free-form `message` if it helps humans, but do not make parsers depend on sentence wording.

---

## 3. Event names beat ad-hoc prose

Prefer:

```text
upload.completed
job.queued
chunk.started
chunk.provider_call_started
chunk.provider_rate_limited
chunk.retry_scheduled
chunk.completed
job.merge_started
job.completed
```

This lets you ask:

```text
show all chunk.retry_scheduled events for job_abc123
```

instead of searching for fourteen phrasings of “trying again.”

---

## 4. Correlation IDs

Your workflow crosses process boundaries:

```text
HTTP request
  ↓
API
  ↓
queue message
  ↓
worker
  ↓
AI provider
```

Use identifiers with different scopes:

```text
request_id → one HTTP interaction
trace_id   → one distributed causal flow
job_id     → one business workflow
chunk_id   → one child unit
message_id → one delivery/event
```

Do not force one ID to mean all five things.

### Queue propagation

A queue message might carry:

```json
{
  "job_id": "job_abc123",
  "chunk_id": "chunk_042",
  "message_id": "evt_9f...",
  "traceparent": "00-...-...-01"
}
```

The worker extracts trace context and creates a new span/events associated with the same distributed flow.

---

## 5. Logging and privacy

Your application processes transcripts, uploaded media and user information.

Do **not** casually log:

- transcript text,
- audio snippets,
- access tokens,
- presigned URLs,
- authorization headers,
- passwords/secrets,
- user email addresses,
- complete third-party API responses that may contain content.

Prefer opaque internal IDs.

```text
job_id=job_abc123
```

is usually far safer operationally than:

```text
email=someone@example.com
transcript="...private conversation..."
```

Apply retention and access control to logs as production data.

---

## 6. Log levels

A practical mental model:

```text
DEBUG → useful during diagnosis; often too noisy for production default
INFO  → normal lifecycle milestones
WARN  → unexpected/recoverable condition
ERROR → operation failed or requires attention
```

Do not log every normal retry as `ERROR` if retry is expected behavior. Otherwise healthy recovery looks like an outage.

---

## 7. Avoid duplicate logging

This stack is noisy enough:

```text
HTTP client logs failure
service logs same failure
worker logs same failure
exception middleware logs same stack
```

Prefer one rich error event at the layer that owns the outcome, plus lower-level detail where genuinely useful.

---

## Exercise — Logging contract

Define log events for:

1. Upload session created.
2. Upload completed.
3. Job published.
4. Chunk started.
5. AI provider returned `429`.
6. Retry scheduled.
7. Chunk completed.
8. Merge claimed.
9. Job completed.
10. Job permanently failed.

For each define:

```text
event name
level
required fields
forbidden/sensitive fields
```

---

## Break it 💥

You receive this production log:

```text
ERROR processing failed
```

List every question you still cannot answer.

Then redesign the event so an engineer can identify:

- job,
- chunk,
- attempt,
- worker,
- dependency,
- normalized failure,
- retry decision,
- trace.

---

## Retrieval quiz

1. Why are structured logs easier to investigate than arbitrary text logs?
2. Difference between `request_id`, `trace_id` and `job_id`?
3. Why should event names be stable?
4. Name four pieces of data you should avoid logging.
5. Why can excessive `ERROR` logging hurt operations?
6. What field would let you jump from a log to a distributed trace?

## Exit criterion

Given only `job_id=abc123`, you can describe exactly which log fields/events would reconstruct the job's lifecycle without exposing transcript content.
