# Week 8 — Answer Key

Use only after attempting the review.

1. Specific events/details for an execution.
2. Stable fields are machine-queryable and aggregatable.
3. HTTP interaction vs distributed causal flow vs business workflow.
4. Example: timestamp, service, event, job_id, chunk_index, attempt, worker_id, trace_id.
5. Stable event names survive prose wording changes and enable reliable queries.
6. Transcript/audio content, secrets/tokens, presigned URLs, emails/PII.
7. It creates noise/alert fatigue and makes expected recovery look catastrophic.
8. Counter monotonically increases; gauge represents current up/down value.
9. A distribution of observed values using buckets/native histogram representation.
10. Averages hide tail latency/outliers.
11. Per-second (or unit-time) change rate of the cumulative counter over the range.
12. Unbounded cardinality creates huge numbers of time series.
13. Number of unique label-value combinations/time series.
14. Rate, Errors, Duration.
15. Queue depth, oldest age, worker utilization, retry rate, completion rate, chunk duration.
16. It lacks arrival rate, service rate and age/context.
17. It distinguishes a harmless deep-but-fast queue from work waiting unacceptably long.
18. Trace = whole distributed operation; span = one operation within it.
19. Moving correlation context across process/service boundaries.
20. Otherwise producer and consumer work appear as unrelated traces.
21. Creates/processes telemetry inside the application and exports it.
22. Receives/processes/routes telemetry to backends.
23. Library/framework coverage vs explicit business-operation spans/metrics.
24. Cost/volume control.
25. Head decides early; tail can decide after observing more/full trace behavior.
26. A representative trace associated with a metric observation.
27. Indicator measurement vs target for that measurement.
28. Internal reliability objective vs external/business agreement.
29. Allowed unreliability under an SLO.
30. Users care about successful/fast workflows, not arbitrary infrastructure utilization.
31. Job start delay, completion success, progress freshness, normalized processing duration.
32. Video lengths differ; raw duration alone misrepresents experience/capacity.
33. Speed at which error budget is being consumed.
34. User-facing success, delay, failure and workflow health.
35. Symptoms represent user impact; causes can be noisy/non-actionable and may not affect users.
36. Clear impact, threshold/window, ownership, context and a concrete next action/runbook.
37. Too many/noisy notifications cause humans to ignore them.
38. Authoritative business/workflow state, typically PostgreSQL for this design.
39. Compare per-job state/logs/traces with fleet/system metrics around the same window.
40. Side effects/artifacts may succeed while the final durable state transition/ACK fails; reconciliation/idempotency is required.
