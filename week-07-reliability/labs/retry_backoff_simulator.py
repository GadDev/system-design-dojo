#!/usr/bin/env python3
import argparse
import random
from collections import Counter


def retry_schedule(clients: int, attempts: int, base: float, cap: float, jitter: str, seed: int):
    random.seed(seed)
    buckets = Counter()
    for _ in range(clients):
        t = 0.0
        for attempt in range(attempts):
            backoff = min(cap, base * (2 ** attempt))
            if jitter == "full":
                wait = random.uniform(0, backoff)
            elif jitter == "equal":
                wait = backoff / 2 + random.uniform(0, backoff / 2)
            else:
                wait = backoff
            t += wait
            buckets[round(t, 1)] += 1
    return buckets


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--clients", type=int, default=200)
    p.add_argument("--attempts", type=int, default=4)
    p.add_argument("--base", type=float, default=1.0)
    p.add_argument("--cap", type=float, default=8.0)
    p.add_argument("--jitter", choices=["none", "full", "equal"], default="full")
    p.add_argument("--seed", type=int, default=7)
    args = p.parse_args()

    buckets = retry_schedule(args.clients, args.attempts, args.base, args.cap, args.jitter, args.seed)
    print(f"clients={args.clients} attempts={args.attempts} jitter={args.jitter}")
    print("retry-time bucket -> attempts")
    for when, count in sorted(buckets.items()):
        print(f"{when:>6.1f}s -> {count}")


if __name__ == "__main__":
    main()
