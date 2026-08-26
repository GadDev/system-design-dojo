#!/usr/bin/env python3
"""Small system-design estimation helper. Values are deliberately assumption-driven."""
from dataclasses import dataclass

SECONDS_PER_DAY = 86_400

@dataclass
class Traffic:
    requests_per_day: float
    peak_factor: float = 5.0

    @property
    def avg_rps(self): return self.requests_per_day / SECONDS_PER_DAY
    @property
    def peak_rps(self): return self.avg_rps * self.peak_factor

def worker_concurrency(units_per_day: float, seconds_per_unit: float, peak_factor: float = 1.0):
    throughput = units_per_day / SECONDS_PER_DAY
    return throughput * seconds_per_unit * peak_factor

if __name__ == '__main__':
    redirects = Traffic(1_000_000_000, 5)
    print(f"URL shortener avg RPS: {redirects.avg_rps:,.0f}")
    print(f"URL shortener peak RPS: {redirects.peak_rps:,.0f}")

    chunks_per_day = 100_000 * 60
    print(f"100k media-hours/day => {chunks_per_day:,.0f} one-minute chunks/day")
    print(f"Avg concurrent chunks @ 15 sec/chunk: {worker_concurrency(chunks_per_day, 15):,.0f}")
    print(f"3x peak concurrent chunks: {worker_concurrency(chunks_per_day, 15, 3):,.0f}")
