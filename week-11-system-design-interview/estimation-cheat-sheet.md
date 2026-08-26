# Back-of-the-Envelope Estimation Cheat Sheet

## Time

```text
1 day = 86,400 seconds ≈ 100k seconds for rough math
```

## Traffic

```text
avg RPS = requests/day ÷ 86,400
peak RPS = avg RPS × explicit peak factor
```

## Storage

```text
bytes/day = objects/day × avg object size
retained bytes = bytes/day × retention days
```

## Bandwidth

```text
bytes/sec × 8 = bits/sec
1 GB/sec ≈ 8 Gbit/sec
```

## Cache

```text
origin QPS = total QPS × miss ratio
```

## Parallel workers

```text
required concurrency ≈ throughput × average duration
```

## Availability intuition

Do not memorize nine-count tables as a substitute for SLO reasoning.

Ask instead:

```text
What user journey is measured?
Over what window?
What failures count?
```

## Rule

If a number does not change a decision, stop calculating it.
