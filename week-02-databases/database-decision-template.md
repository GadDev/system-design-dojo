# Database Decision Record

## Decision

<!-- One sentence. Example: Store canonical transcript artifacts in object storage and searchable segment metadata in PostgreSQL. -->

## Status

```text
Proposed | Accepted | Superseded
```

## Context

### Product requirement

### Dominant reads

### Dominant writes

### Consistency requirement

### Expected data size / growth

### Retention

### Latency expectations

---

# Options considered

## Option A

### Benefits

### Costs

### Failure modes

### Operational complexity

## Option B

### Benefits

### Costs

### Failure modes

### Operational complexity

## Option C

### Benefits

### Costs

### Failure modes

### Operational complexity

---

# Evidence

What production measurements or requirements support this decision?

```text
query rate:
row count:
data size:
p95 / p99:
DB CPU:
DB I/O:
connection pressure:
replica lag tolerance:
```

---

# Decision

Explain the chosen option and why the rejected options are not appropriate **for the current requirements**.

---

# Revisit triggers

What evidence would make us reconsider?

Examples:

```text
transcript storage exceeds X TB
DB backup time exceeds target
read p99 exceeds SLO
primary read I/O > threshold
chunk table > retention/maintenance threshold
single-node write ceiling reached
```

A good architecture decision has an escape hatch.
