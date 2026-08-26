# Day 4 — SLIs, SLOs, SLAs & Error Budgets

## Goal

Turn telemetry into **reliability objectives based on user experience**, not arbitrary infrastructure thresholds.

---

## 1. Four terms

### SLI — Service Level Indicator

A measured indicator of behavior.

Examples:

```text
successful job completion ratio
API request success ratio
job time-to-start
transcription completion duration
progress freshness
```

### SLO — Service Level Objective

A target for an SLI.

Illustrative example:

```text
99.9% of GET /jobs requests succeed over 30 days
```

### SLA — Service Level Agreement

An external/business agreement, often including consequences when guarantees are not met.

### Error budget

If your SLO allows some unreliability, that allowance is the error budget.

```text
100% target
-
99.9% SLO
=
0.1% budget
```

---

## 2. Infrastructure metrics are not automatically SLIs

This:

```text
CPU < 80%
```

is not usually a customer-facing reliability objective.

A customer cares about:

```text
Can I upload?
Did my job start?
Is progress moving?
Did my transcript finish?
Can I retrieve the result?
```

CPU is diagnostic evidence.

---

## 3. Candidate transcription SLIs

### API availability

```text
successful eligible API requests
/
total eligible API requests
```

### Job acceptance

```text
accepted durable jobs
/
valid submission attempts
```

### Time to start

```text
time first chunk starts
-
time job accepted
```

### Completion success

```text
jobs completed successfully
/
jobs expected to complete
```

### Processing latency

Raw duration can be misleading because videos vary in length.

Consider a normalized ratio:

```text
processing_duration
/
media_duration
```

A 120-minute video taking 20 minutes and a 5-minute video taking 20 minutes are very different experiences.

### Progress freshness

```text
now - last_progress_update
```

This is surprisingly useful for detecting stuck workflows.

---

## 4. Example SLO document

These numbers are **illustrative**, not product commitments:

```text
SLO A — Job status API
99.9% successful eligible requests over rolling 30 days.

SLO B — Job start
95% of accepted jobs start processing within 5 minutes.

SLO C — Completion
99% of valid jobs complete without manual intervention.

SLO D — Progress freshness
99% of processing jobs emit a progress/state update within 10 minutes.
```

Your actual numbers must come from product expectations, capacity and cost.

---

## 5. Error-budget reasoning

Suppose:

```text
SLO = 99.9%
```

Over 30 days the failure allowance is 0.1% of eligible events/time, depending on how the SLI is defined.

Do not immediately translate every SLO into “five nines.” Higher reliability costs money and can slow delivery.

The senior question is:

> What reliability does the user/business need, and what are we willing to spend to achieve it?

---

## 6. Burn rate

A burn-rate alert asks:

> How quickly are we consuming the error budget?

This is often more meaningful than alerting on every isolated error.

A short, severe outage burns budget quickly.

A tiny persistent error rate burns it slowly.

Both may matter differently.

---

## Exercise — Write your first SLOs

Define 3–5 SLIs/SLOs for the transcription application.

For each:

```text
User promise/question
SLI formula
SLO target
measurement window
excluded traffic
source telemetry
why this target matters
```

At least one must describe **asynchronous workflow health**, not HTTP availability.

---

## Break it 💥

The team proudly reports:

```text
API uptime = 99.99%
```

but 15% of transcription jobs remain queued for three hours.

Explain why the service can have excellent HTTP availability and terrible product reliability.

---

## Retrieval quiz

1. SLI vs SLO vs SLA?
2. What is an error budget?
3. Why is CPU usage usually not a good user-facing SLI?
4. Why normalize transcription duration by media duration?
5. What does progress freshness detect?
6. What does burn rate tell you?

## Exit criterion

You can define reliability objectives that describe whether users can successfully complete transcription workflows—not just whether containers are alive.
