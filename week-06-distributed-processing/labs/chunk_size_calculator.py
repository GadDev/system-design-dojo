#!/usr/bin/env python3
import argparse
import math

DEFAULTS = [30, 60, 120, 300]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--duration-minutes", type=float, default=90)
    p.add_argument("--overhead-ms", type=float, default=150)
    args = p.parse_args()

    total_seconds = args.duration_minutes * 60
    print(f"Media duration: {args.duration_minutes:.1f} min\n")
    print(f"{'chunk':>8} {'tasks':>8} {'fixed overhead':>18} {'retry domain':>14}")
    for size in DEFAULTS:
        tasks = math.ceil(total_seconds / size)
        overhead_seconds = tasks * args.overhead_ms / 1000
        print(f"{size:>7}s {tasks:>8} {overhead_seconds:>16.2f}s {size:>12}s")

if __name__ == "__main__":
    main()
