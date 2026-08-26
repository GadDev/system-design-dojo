# Week 8 — Sources & Reading Map 📚

Use primary documentation first. The goal is not to memorize an observability vendor; it is to build a durable mental model of telemetry and production diagnosis.

---

## Day 1 — Logs & correlation

### OpenTelemetry — Signals

https://opentelemetry.io/docs/concepts/signals/

Read for the distinction between traces, metrics, logs and baggage.

### OpenTelemetry — Logs specification

https://opentelemetry.io/docs/specs/otel/logs/

Focus on log/trace correlation using trace and span context.

### OpenTelemetry — Context propagation

https://opentelemetry.io/docs/concepts/context-propagation/

Focus on why context must cross service/process boundaries.

---

## Day 2 — Metrics & Prometheus

### Prometheus — Metric types

https://prometheus.io/docs/concepts/metric_types/

Focus on counters, gauges and histograms.

### Prometheus — Instrumentation practices

https://prometheus.io/docs/practices/instrumentation/

Focus on online services vs offline workers and label cardinality.

### Prometheus — Metric/label naming

https://prometheus.io/docs/practices/naming/

Pay particular attention to the warning about high-cardinality labels such as user IDs.

### Prometheus — Histograms and summaries

https://prometheus.io/docs/practices/histograms/

Understand why distributions/percentiles matter for latency.

---

## Day 3 — Distributed tracing & OpenTelemetry

### OpenTelemetry — Observability primer

https://opentelemetry.io/docs/concepts/observability-primer/

### OpenTelemetry — Python

https://opentelemetry.io/docs/languages/python/

### OpenTelemetry — Python instrumentation

https://opentelemetry.io/docs/languages/python/instrumentation/

### OpenTelemetry Collector quick start

https://opentelemetry.io/docs/collector/quick-start/

### W3C Trace Context

https://www.w3.org/TR/trace-context/

Focus on `traceparent` conceptually; do not memorize the wire format.

---

## Day 4 — SLIs / SLOs / error budgets

### Google SRE — Service Level Objectives

https://sre.google/sre-book/service-level-objectives/

### Google SRE Workbook — Implementing SLOs

https://sre.google/workbook/implementing-slos/

Read for user-oriented SLIs, target selection and error-budget reasoning.

---

## Day 5 — Grafana & alerting

### Grafana — Alerting

https://grafana.com/docs/grafana/latest/alerting/

### Grafana — Exemplars

https://grafana.com/docs/grafana/latest/fundamentals/exemplars/

Focus on moving from aggregate metrics to representative traces.

### Grafana Tempo — Visualize traces

https://grafana.com/docs/tempo/latest/visualize-traces/

### Google SRE — Monitoring Distributed Systems

https://sre.google/sre-book/monitoring-distributed-systems/

Pay attention to the four golden signals and the distinction between symptoms and causes.

---

## Day 6 — Incident investigation

### Google SRE — Practical Alerting

https://sre.google/sre-book/practical-alerting/

### Google SRE Workbook — Alerting on SLOs

https://sre.google/workbook/alerting-on-slos/

Then do the stuck-job lab **before** searching for more incident playbooks.

---

# Books

## Site Reliability Engineering — Google

Free online:

https://sre.google/sre-book/table-of-contents/

Week 8 focus:

- Monitoring Distributed Systems
- Service Level Objectives
- Practical Alerting from Time-Series Data

## The Site Reliability Workbook — Google

Free online:

https://sre.google/workbook/table-of-contents/

Week 8 focus:

- Implementing SLOs
- Monitoring
- Alerting on SLOs

## Observability Engineering — Charity Majors, Liz Fong-Jones, George Miranda

Use as a conceptual companion for high-cardinality event data, exploratory debugging and observability culture.

Do not treat any specific vendor examples as architectural requirements.

## Distributed Systems Observability — Cindy Sridharan

Useful short-form material for logs, metrics and tracing mental models.

---

# Reading strategy

For every source, write three sentences:

```text
This signal/mechanism tells me ______.
It does NOT tell me ______.
In the transcription pipeline I would use it when ______.
```

That prevents “observability = install Grafana” thinking.
