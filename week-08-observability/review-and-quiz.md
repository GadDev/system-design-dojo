# Week 8 — 40-Question Review

Answer without notes first.

## Logs & correlation

1. What question are logs best at answering?
2. Why prefer structured logs over arbitrary prose?
3. Difference between `request_id`, `trace_id` and `job_id`?
4. Give five stable fields for a worker log event.
5. Why use stable event names?
6. Name four types of sensitive data you should not casually log.
7. Why can logging every retry as ERROR be harmful?

## Metrics & Prometheus

8. Counter vs gauge?
9. What is a histogram?
10. Why is average latency insufficient?
11. What does `rate(counter[5m])` conceptually tell you?
12. Why is `job_id` a bad Prometheus label?
13. What is metric cardinality?
14. Name the RED signals.
15. Name four worker/pipeline metrics.
16. Why is queue depth insufficient by itself?
17. What does oldest queued job age add?

## Tracing & OpenTelemetry

18. Trace vs span?
19. What is context propagation?
20. Why must trace context cross queue messages?
21. What does the OpenTelemetry SDK do conceptually?
22. What does the Collector do?
23. Auto vs manual instrumentation?
24. Why sample traces?
25. Head vs tail sampling at a high level?
26. What is an exemplar?

## SLOs

27. SLI vs SLO?
28. SLO vs SLA?
29. What is an error budget?
30. Why is CPU usually not a user-facing SLI?
31. Give two useful async-transcription SLIs.
32. Why normalize processing time by media duration?
33. What is burn rate?

## Dashboards & alerts

34. What should a product-health dashboard show first?
35. Why should paging alerts prefer symptoms?
36. What makes an alert actionable?
37. What is alert fatigue?

## Incident investigation

38. What is your first source when investigating one stuck job?
39. How do you distinguish a single-job failure from a systemic incident?
40. Why can a job remain PROCESSING even when all expensive computation already succeeded?

---

## Score

| Score | Meaning |
|---|---|
| 36–40 | Strong — you can begin incident-style system design |
| 31–35 | Good — review 2–3 weak areas |
| 24–30 | Re-run labs and SLO/dashboard exercises |
| <24 | Rebuild the logs → metrics → traces investigation path |
