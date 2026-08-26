# Integration Event Contract Template

## Identity

- Event type:
- Version:
- Producer:
- Aggregate/entity:

## Meaning

What business fact has already happened?

## Schema

```json
{
  "event_id": "",
  "event_type": "",
  "occurred_at": "",
  "aggregate_id": "",
  "aggregate_version": 0
}
```

## Consumers

| Consumer | Why it needs the event | Max acceptable lag |
|---|---|---|
| | | |

## Delivery contract

- delivery semantics:
- ordering scope:
- duplicate handling:
- retry policy:
- DLQ/recovery:

## Consistency

- authoritative source:
- when is the event published relative to the DB commit?
- outbox required?

## Privacy / security

- PII included?
- sensitive fields?
- retention?

## Evolution

- compatibility strategy:
- deprecated fields:
- minimum supported consumer version:
