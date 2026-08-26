# Incident Investigation Template

## Report

```text
Reporter:
Time reported:
Affected job/tenant:
User-visible symptom:
```

## 1. Authoritative state

```text
job status:
current stage:
last durable update:
completed/expected chunks:
```

## 2. Scope

```text
single job / tenant / region / global:
arrival rate:
completion rate:
queue age:
error/retry rate:
```

## 3. Timeline

| Time | Evidence | Event |
|---|---|---|
| | | |

## 4. Trace findings

```text
trace_id:
slowest span:
failed span:
queue wait:
worker duration:
```

## 5. Logs

```text
last successful event:
last error/warning:
retry state:
worker/message identifiers:
```

## 6. Hypotheses

### Leading hypothesis

```text
...
```

### Evidence supporting

```text
...
```

### Evidence contradicting

```text
...
```

## 7. Mitigation

```text
...
```

## 8. Recovery proof

What telemetry/state proves normal behavior has returned?

## 9. User communication

```text
...
```

## 10. Follow-up

```text
instrumentation gap:
alert/dashboard gap:
architecture fix:
owner:
```
