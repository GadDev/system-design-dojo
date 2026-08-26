# Practice 02 — Pastebin 🟢

## Prompt

> Design a text-paste sharing service.

## Requirement cards

- pastes up to 1 MB
- public or unlisted
- optional expiration
- mostly immutable after creation
- 20M reads/day, 1M writes/day

## Main lesson

```text
metadata vs content storage
```

## Questions

- Put text directly in PostgreSQL?
- Put large pastes in object storage?
- Cache popular pastes?
- How does expiration cleanup work?
- How do you prevent abuse/malware/phishing content?

## Deep dive

Compare:

```text
PostgreSQL text
vs
object storage + metadata DB
vs
hybrid threshold
```

Discuss backup, search, retention, read latency and cost.
