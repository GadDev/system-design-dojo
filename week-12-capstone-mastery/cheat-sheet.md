# Week 12 — Final System Design Cheat Sheet 🥷

## The seven steps

```text
Requirements
Estimates
API
Data
Architecture
Bottlenecks
Tradeoffs
```

## Cross-cutting pass

```text
Failure
Security/privacy
Observability
Cost
Consistency
Operations
```

## Workload signatures

```text
URL shortener → hot reads / cache
Pastebin → object/text storage + retention
Rate limiter → distributed counters
Notifications → queue + provider isolation
File upload → data plane bypass
Chat → connection state + durable messages
Transcription → fan-out/fan-in + retry domain
YouTube → transcode + CDN
Feed → fan-out tradeoff
Uber → geospatial + realtime
Dropbox → sync + reconciliation
Netflix → bandwidth + edge locality
```

## Source of truth questions

```text
Which fact?
Which authority?
Which derived copies?
How stale?
How reconcile?
```

## Scaling questions

```text
What is saturated?
What metric proves it?
What is the smallest change?
What failure mode does the change add?
```

## Async questions

```text
At-least-once?
Idempotent?
ACK when?
Retry what?
DLQ owner?
Backpressure?
Fairness?
```

## Final tradeoff phrase

> “Given requirement X and scale Y, I choose A over B because Z. The cost is C, and I would revisit this if metric/requirement T appears.”
