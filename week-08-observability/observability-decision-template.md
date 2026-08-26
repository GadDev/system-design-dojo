# Observability Decision Record

## Context

What production question or failure mode are we trying to make diagnosable?

## User impact

What would the user experience?

## Source of truth

Which durable system tells us the authoritative business state?

## Logs

### Events

```text
...
```

### Required fields

```text
...
```

### Sensitive fields explicitly forbidden

```text
...
```

### Retention / access

```text
...
```

## Metrics

| Metric | Type | Labels | Question answered |
|---|---|---|---|
| | | | |

### Cardinality budget

Which dimensions are bounded? Which identifiers are prohibited as labels?

## Traces

### Critical spans

```text
...
```

### Propagation boundaries

```text
HTTP → queue → worker → dependency
```

### Sampling

```text
...
```

## SLIs / SLOs

| SLI | Formula | SLO | Window |
|---|---|---|---|
| | | | |

## Dashboards

```text
product health
pipeline health
dependencies
```

## Alerts

For each alert:

```text
symptom
threshold/window
severity
owner
runbook
expected action
```

## Cost / volume

What is the estimated log, metric-series and trace volume at 10× and 100× scale?

## Privacy / security

What data must never be exported to telemetry backends?

## Failure modes of observability itself

What happens if telemetry export is unavailable? Must application traffic continue?

## Review trigger

What evidence would cause us to redesign instrumentation, retention or alerting?
