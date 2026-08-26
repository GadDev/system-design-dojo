# Day 3 — Distributed Tracing & OpenTelemetry

## Goal

Follow one workflow across process and network boundaries, and understand what OpenTelemetry contributes to logs, metrics and traces.

---

## 1. Trace vs span

A **trace** represents one distributed operation.

A **span** represents one unit of work inside that operation.

```text
Trace: create transcription job
│
├── HTTP POST /uploads/{id}/complete
├── PostgreSQL INSERT job
├── publish queue event
└── worker consume
     ├── fetch object metadata
     ├── call AI provider
     └── persist chunk result
```

Spans contain attributes such as:

```text
service.name
operation
start/end time
status
error
selected bounded attributes
```

---

## 2. Context propagation

Tracing becomes distributed only if context crosses boundaries.

HTTP is straightforward:

```text
Client
  ↓ trace context header
API
  ↓ trace context header
Service
```

Queues need explicit attention:

```text
API span
  ↓ inject context into message headers
Queue
  ↓ extract context
Worker span
```

OpenTelemetry's default propagation commonly uses W3C Trace Context (`traceparent`).

---

## 3. Async causality

A worker may start seconds or minutes after publication.

Conceptually:

```text
producer span
    ↓
message waiting
    ↓
consumer processing span
```

You want to distinguish:

```text
queue delay
```

from:

```text
worker processing duration
```

Otherwise a 12-minute end-to-end trace may make a healthy 20-second worker look slow.

---

## 4. OpenTelemetry mental model

```text
Application
   ↓ instrumentation
OTel API / SDK
   ↓
Exporter
   ↓
OTel Collector
   ↓
Backend(s)
```

The Collector can receive, process and export telemetry to one or more backends.

This gives you a vendor-neutral instrumentation layer.

---

## 5. Auto vs manual instrumentation

Auto/library instrumentation is excellent for:

```text
HTTP server spans
HTTP client spans
DB client spans
framework operations
```

Manual instrumentation is still valuable for **business operations**:

```text
transcription.chunk
transcription.merge
transcription.prepare_audio
```

A trace containing 300 generic `HTTP POST` spans but no concept of “chunk 42” is technically instrumented and operationally annoying.

---

## 6. Add useful span attributes

Good bounded attributes might include:

```text
transcription.stage="chunk"
transcription.model="model_a"
transcription.chunk_index=42
retry.attempt=2
error.type="rate_limited"
```

Be careful with:

```text
user email
transcript content
full presigned URL
secret token
```

High-cardinality attributes are more acceptable in traces than Prometheus labels, but still affect cost and privacy.

---

## 7. Sampling

Tracing every operation forever can be expensive.

Sampling strategies include:

```text
head sampling
→ decision near trace start

tail sampling
→ decision after seeing more of the trace
```

Tail sampling can preserve interesting traces such as errors or high-latency executions, but requires more collector/backend machinery.

Always think:

```text
telemetry value
vs
telemetry cost
```

---

## 8. Correlate all three signals

Ideal workflow:

```text
Metric:
AI 429 rate spikes
      ↓
Exemplar / trace link
      ↓
Trace:
AI span spent 8s + rate limited
      ↓
Log:
job_id=abc123 chunk=42 retry scheduled in 8.4s
```

This is far more useful than three isolated observability products.

---

## Exercise — Design the trace

Design spans for:

```text
POST upload complete
 ↓
create job
 ↓
publish queue message
 ↓
prepare audio
 ↓
fan-out chunks
 ↓
chunk 42 transcription
 ↓
merge
```

For every span specify:

```text
name
parent/link
attributes
error status
which IDs propagate
```

---

## Break it 💥

Your API trace ends at `publish_message`.

The worker starts a completely unrelated trace.

A customer job takes 25 minutes.

Explain what investigation capability you lost and how to restore it.

---

## Retrieval quiz

1. Trace vs span?
2. What is context propagation?
3. Why is queue wait time different from worker duration?
4. What does the OpenTelemetry Collector do?
5. Auto vs manual instrumentation?
6. Why sample traces?
7. What is an exemplar conceptually?

## Exit criterion

You can draw one causal trace from API request through queue and worker, while keeping business identifiers, privacy and sampling considerations explicit.
