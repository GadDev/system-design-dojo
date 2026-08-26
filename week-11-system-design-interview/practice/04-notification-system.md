# Practice 04 — Notification System 🟡

## Prompt

> Design a platform that sends email, SMS and push notifications for many product teams.

## Requirement cards

- transactional + bulk notifications
- user channel preferences
- retries
- priority tiers
- provider rate limits
- delivery status

## Main lesson

```text
async queues + provider isolation
```

## Deep dive

```text
API → durable request → queue/router
                   ├→ email workers
                   ├→ SMS workers
                   └→ push workers
```

Questions:

- What prevents duplicate SMS?
- What is authoritative delivery status?
- How do retries differ for 429 vs invalid number?
- One global queue or per-channel/priority queues?
- What happens when one provider is down?
