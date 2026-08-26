#!/usr/bin/env python3
"""Tiny queue-capacity calculator for Week 5 exercises."""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arrival-per-hour", type=float, required=True)
    parser.add_argument("--worker-throughput-per-hour", type=float, required=True)
    parser.add_argument("--workers", type=int, required=True)
    parser.add_argument("--starting-backlog", type=float, default=0)
    parser.add_argument("--hours", type=float, default=1)
    args = parser.parse_args()

    capacity = args.worker_throughput_per_hour * args.workers
    net = args.arrival_per_hour - capacity
    ending = max(0.0, args.starting_backlog + net * args.hours)

    print(f"arrival rate      : {args.arrival_per_hour:.2f} jobs/hour")
    print(f"worker capacity   : {capacity:.2f} jobs/hour")
    print(f"net backlog rate  : {net:+.2f} jobs/hour")
    print(f"ending backlog    : {ending:.2f} jobs")

    if net > 0:
        print("result             : backlog grows under sustained load")
    elif net < 0:
        print("result             : spare capacity can drain backlog")
        if args.starting_backlog > 0:
            drain_rate = -net
            print(f"drain time estimate: {args.starting_backlog / drain_rate:.2f} hours")
    else:
        print("result             : exactly at theoretical capacity; no safety margin")


if __name__ == "__main__":
    main()
