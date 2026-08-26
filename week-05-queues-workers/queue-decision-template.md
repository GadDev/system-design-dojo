# Queue / Messaging Architecture Decision Record

## Decision

```text
Status: Proposed / Accepted / Superseded
Date:
Owner:
```

## Context

What long-running or decoupled workflow are we solving?

## Functional requirements

- 
- 
- 

## Non-functional requirements

```text
Expected publish rate:
Peak rate:
Average processing time:
Maximum acceptable queue wait:
Durability requirement:
Ordering requirement:
Replay requirement:
Retention requirement:
```

## Business state source of truth

```text
PostgreSQL / broker log / other
```

Why?

## Message schema

```json
{}
```

### Message identity

```text
message_id:
logical operation id:
schema version:
```

## Delivery semantics

```text
At-most-once / at-least-once / scoped exactly-once
```

Why?

## Acknowledgement point

When exactly does the consumer ACK/commit its progress?

## Idempotency strategy

- unique constraints:
- conditional state transitions:
- processed-message/inbox record:
- provider idempotency keys:
- reconciliation:

## DB → broker publication boundary

```text
Direct publish / transactional outbox / CDC / other
```

What crash window remains?

## Retry policy

| Failure class | Retry? | Delay/backoff | Max attempts | Max age | Final action |
|---|---|---|---:|---:|---|
| | | | | | |

## Dead-letter policy

```text
DLQ destination:
Owner:
Alert threshold:
Retention:
Redrive process:
```

## Ordering

What needs to be ordered?

```text
Global / per user / per job / none
```

How is that enforced?

## Worker concurrency

```text
Per worker:
Global:
Per user/tenant:
Per dependency:
```

## Broker candidates

| Requirement | Redis Streams | RabbitMQ | Kafka |
|---|---|---|---|
| | | | |

## Selected option

What did we choose and why?

## Rejected alternatives

### Alternative A

Why not now?

### Alternative B

Why not now?

## Metrics / SLOs

```text
queue depth:
oldest-message age:
publish failures:
processing p95:
redelivery rate:
DLQ rate:
end-to-end completion p95:
```

## Backpressure / overload policy

What happens when consumers fall behind?

## Security / privacy

What data is permitted in messages?

How are credentials/access to storage handled?

## Cost

What costs scale with:

- messages,
- retention,
- worker time,
- retries,
- duplicate work?

## Migration triggers

What evidence would justify changing broker or architecture?

Examples:

```text
Need durable replay for many teams
Need sophisticated routing
Need 10× throughput
Need stronger HA
Operations burden too high
DLQ/retry needs outgrow current system
```
