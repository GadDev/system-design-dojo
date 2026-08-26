# Day 6 — Training Ladder: Levels 1–6 🥋

## Goal

Run six compressed design drills using the **same seven steps** every time.

Do not read the reference notes first.

---

# Drill format

For each system:

```text
5 min  Requirements + estimation
4 min  API + data
6 min  architecture
3 min  10× bottleneck
2 min  tradeoff conclusion
```

Total:

```text
~20 minutes/system
```

If six in one day is too much, do three today and three tomorrow before the full mock.

---

# 🟢 Level 1 — URL Shortener

Main lesson:

```text
DB + cache + hot keys
```

Questions you should reach naturally:

- redirect latency target?
- read/write ratio?
- custom alias?
- expiration?
- immutable vs editable targets?
- hot celebrity links?

Deep dive:

```text
cache-aside
negative caching
DB index on short_code
TTL bounded by link expiration
edge caching tradeoff
```

Brief: [`practice/01-url-shortener.md`](practice/01-url-shortener.md)

---

# 🟢 Level 2 — Pastebin

Main lesson:

```text
metadata vs blob/text storage
```

Questions:

- max paste size?
- retention?
- public/private?
- edit after creation?
- read/write ratio?

Deep dive:

```text
object storage vs DB text
content ID
cache
expiration cleanup
abuse controls
```

Brief: [`practice/02-pastebin.md`](practice/02-pastebin.md)

---

# 🟢 Level 3 — Rate Limiter

Main lesson:

```text
distributed counters + correctness/performance
```

Deep dive:

```text
token bucket
sliding window
Redis atomicity
local vs global limiter
failure policy
hot tenants
```

Brief: [`practice/03-rate-limiter.md`](practice/03-rate-limiter.md)

---

# 🟡 Level 4 — Notification System

Main lesson:

```text
queues + retry + provider isolation
```

Deep dive:

```text
email / push / SMS
user preferences
priority queues
at-least-once
idempotency
provider rate limits
DLQ
```

Brief: [`practice/04-notification-system.md`](practice/04-notification-system.md)

---

# 🟡 Level 5 — File Upload Service

Main lesson:

```text
control plane vs data plane
```

Deep dive:

```text
multipart/resumable upload
object storage
checksums
completion idempotency
cleanup
malware scanning
```

Brief: [`practice/05-file-upload-service.md`](practice/05-file-upload-service.md)

---

# 🟡 Level 6 — Chat System

Main lesson:

```text
persistent connections + online/offline delivery
```

Deep dive:

```text
WebSocket connection gateway
message durability
ordering scope
presence
reconnect
history
fan-out
```

Brief: [`practice/06-chat-system.md`](practice/06-chat-system.md)

---

# After every drill

Write only three sentences:

```text
My main design decision:
My weakest assumption:
The first thing I'd improve at 10×:
```

That creates a feedback loop without writing a novel after every mock.

---

## Exit criterion

You can apply the same framework to six different workloads without forcing them into the same architecture.
