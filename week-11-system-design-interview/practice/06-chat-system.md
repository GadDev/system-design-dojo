# Practice 06 — Chat System 🟡

## Prompt

> Design a realtime 1-to-1 and group chat system.

## Requirement cards

- 10M DAU
- message history
- online/offline users
- multi-device
- read receipts optional
- media attachments separate

## Main lesson

```text
connection state + durable message state
```

## Deep dive

```text
Client ⇄ WebSocket Gateway
              ↓
        Message Service
              ↓
        Durable Store
              ↓
          Fan-out
```

Questions:

- ordering scope?
- reconnect semantics?
- client-generated message IDs?
- duplicate sends?
- offline delivery?
- presence accuracy?
- what state belongs in gateway memory vs durable storage?
