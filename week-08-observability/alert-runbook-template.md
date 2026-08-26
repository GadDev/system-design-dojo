# Alert Runbook Template

## Alert

```text
name:
severity:
owner:
```

## User symptom

What user-visible behavior does this alert approximate?

## Trigger

```text
query:
threshold:
window:
```

## Why this threshold exists

What evidence or SLO connects the threshold to meaningful impact?

## First 5 minutes

1. Confirm alert is still firing.
2. Check product-health/SLO panel.
3. Determine scope: single job / tenant / region / global.
4. Check recent deployments/config changes.
5. Inspect the dependency/pipeline dashboard indicated below.

## Diagnostic queries

### Metrics

```promql
...
```

### Logs

```text
...
```

### Traces

```text
...
```

## Likely causes

- ...

## Safe mitigations

- ...

## Dangerous mitigations

- ...

## Recovery proof

What signal proves the system has returned to acceptable behavior?

## Escalation

```text
when:
to whom:
what context to include:
```

## Follow-up

After the incident, ask whether the alert detected a **symptom early enough** and whether the runbook reduced time-to-diagnosis.
