"""Tiny Week 4 capacity worksheet.

Change assumptions and observe how control-plane and media-plane scale differ.
"""

from dataclasses import dataclass


@dataclass
class UploadBurst:
    users: int = 10_000
    average_file_gb: float = 1.0
    burst_minutes: float = 15.0
    init_window_seconds: float = 60.0
    parts_per_file: int = 20
    concurrent_parts_per_client: int = 4

    @property
    def total_media_tb(self) -> float:
        return self.users * self.average_file_gb / 1000

    @property
    def aggregate_gbit_s(self) -> float:
        total_gbit = self.users * self.average_file_gb * 8
        return total_gbit / (self.burst_minutes * 60)

    @property
    def init_rps(self) -> float:
        return self.users / self.init_window_seconds

    @property
    def max_simultaneous_part_transfers(self) -> int:
        return self.users * self.concurrent_parts_per_client


def main() -> None:
    burst = UploadBurst()
    print(f"Total media: ~{burst.total_media_tb:.1f} TB")
    print(f"Aggregate media rate: ~{burst.aggregate_gbit_s:.1f} Gbit/s")
    print(f"Upload-init requests: ~{burst.init_rps:.1f} RPS")
    print(
        "Potential part transfers in flight: "
        f"{burst.max_simultaneous_part_transfers:,}"
    )


if __name__ == "__main__":
    main()
