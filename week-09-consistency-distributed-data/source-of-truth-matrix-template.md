# Source-of-Truth Matrix Template

Use one row per **fact**, not per technology.

| Fact | Authority | Writers | Derived copies | Consistency requirement | Divergence detection | Repair |
|---|---|---|---|---|---|---|
| | | | | | | |

## Prompts

For each row:

```text
What exactly is the fact?
Who is allowed to write it?
Can two actors write concurrently?
Which copy wins during disagreement?
How stale may readers be?
What invariant proves correctness?
What telemetry detects divergence?
Can repair be automatic?
```
