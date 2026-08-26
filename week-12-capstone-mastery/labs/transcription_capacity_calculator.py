#!/usr/bin/env python3
"""Capacity sketch for the 100k media-hours/day final exercise."""
from dataclasses import dataclass

SECONDS_PER_DAY = 86_400

@dataclass
class Model:
    media_hours_per_day: float = 100_000
    chunk_seconds: int = 60
    processing_seconds_per_chunk: float = 15.0
    peak_factor: float = 3.0
    avg_upload_mbps: float = 2.0

    @property
    def chunks_per_day(self):
        return self.media_hours_per_day * 3600 / self.chunk_seconds

    @property
    def avg_chunks_per_sec(self):
        return self.chunks_per_day / SECONDS_PER_DAY

    @property
    def avg_concurrency(self):
        return self.avg_chunks_per_sec * self.processing_seconds_per_chunk

    @property
    def peak_concurrency(self):
        return self.avg_concurrency * self.peak_factor

    @property
    def raw_media_tb_per_day(self):
        bits = self.media_hours_per_day * 3600 * self.avg_upload_mbps * 1_000_000
        return bits / 8 / 1_000_000_000_000

if __name__ == '__main__':
    m = Model()
    print(f"Media hours/day: {m.media_hours_per_day:,.0f}")
    print(f"Chunks/day: {m.chunks_per_day:,.0f}")
    print(f"Average chunks/sec: {m.avg_chunks_per_sec:,.1f}")
    print(f"Average worker concurrency: {m.avg_concurrency:,.0f}")
    print(f"Peak worker concurrency ({m.peak_factor}x): {m.peak_concurrency:,.0f}")
    print(f"Raw media/day @ {m.avg_upload_mbps:g} Mbps avg bitrate: {m.raw_media_tb_per_day:,.1f} TB")
