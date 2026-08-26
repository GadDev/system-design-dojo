# Week 11 — Sources & Reading Map

The point of this week is practice, not collecting more theory. Read selectively.

## Core interview-process references

### System Design Primer

- https://github.com/donnemartin/system-design-primer

Why: open-source collection with an interview approach built around use cases, constraints, assumptions, high-level design and bottleneck discussion.

### ByteByteGo — interview framework

- https://bytebytego.com/courses/system-design-interview/a-framework-for-system-design-interviews
- https://bytebytego.com/guides/how-to-ace-system-design-interviews-like-a-boss/

Use as a secondary worked framework. Do not memorize sample architectures.

---

## Architecture review references

### AWS Well-Architected Framework

- https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html

Use the six pillars as a cross-check: operational excellence, security, reliability, performance efficiency, cost optimization and sustainability.

### Google SRE

- https://sre.google/sre-book/table-of-contents/

Revisit latency, overload, monitoring, SLOs and capacity reasoning.

---

## API / retry semantics

### HTTP Semantics — RFC 9110

- https://www.rfc-editor.org/rfc/rfc9110.html

Focus on safe/idempotent methods and conditional requests.

---

## Practice-system references

### Rate limiting

- Redis patterns: https://redis.io/docs/latest/commands/incr/

### Large uploads

- Cloudflare R2: https://developers.cloudflare.com/r2/objects/multipart-objects/
- YouTube resumable protocol: https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol

### Chat / realtime

- MDN WebSocket API: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API

---

## Reading schedule

```text
Day 1 → System Design Primer interview approach
Day 2 → back-of-envelope estimation material + your own worksheet
Day 3 → RFC 9110 only where API semantics matter
Day 4 → AWS Well-Architected performance/reliability cross-check
Day 5 → ByteByteGo framework after writing your own decision narrative
Day 6 → no broad reading; do the six drills
Day 7 → no reading before the mock
```

## Book focus

- **System Design Interview, Vol. 1 & 2 — Alex Xu / Sahn Lam**: compare after solving problems yourself.
- **Designing Data-Intensive Applications, 2nd Edition**: tradeoff depth, not interview scripts.
- **Site Reliability Engineering**: reliability/operability lens.

Every practice session should end with:

> **“Which requirement drove each major component, and which component did I add without enough evidence?”**
