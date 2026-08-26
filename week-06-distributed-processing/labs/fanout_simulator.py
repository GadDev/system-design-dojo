#!/usr/bin/env python3
import argparse
import asyncio
import random
import statistics
import time

async def process_chunk(index: int, semaphore: asyncio.Semaphore, failure_rate: float, max_retries: int):
    attempts = 0
    started = time.perf_counter()
    while True:
        attempts += 1
        async with semaphore:
            service = random.uniform(0.05, 0.25)
            # Create occasional stragglers.
            if random.random() < 0.03:
                service *= random.uniform(4, 8)
            await asyncio.sleep(service)
            failed = random.random() < failure_rate
        if not failed:
            return {
                "index": index,
                "attempts": attempts,
                "elapsed": time.perf_counter() - started,
            }
        if attempts > max_retries:
            raise RuntimeError(f"chunk {index} failed after {attempts} attempts")
        await asyncio.sleep(0.02 * (2 ** (attempts - 1)))

async def main(args):
    semaphore = asyncio.Semaphore(args.concurrency)
    t0 = time.perf_counter()
    results = await asyncio.gather(
        *(process_chunk(i, semaphore, args.failure_rate, args.max_retries) for i in range(args.chunks)),
        return_exceptions=True,
    )
    elapsed = time.perf_counter() - t0
    successes = [r for r in results if isinstance(r, dict)]
    failures = [r for r in results if isinstance(r, Exception)]
    durations = [r["elapsed"] for r in successes]
    retries = sum(r["attempts"] - 1 for r in successes)

    print(f"chunks:       {args.chunks}")
    print(f"concurrency:  {args.concurrency}")
    print(f"elapsed:      {elapsed:.3f}s")
    print(f"successes:    {len(successes)}")
    print(f"failures:     {len(failures)}")
    print(f"retries:      {retries}")
    if durations:
        print(f"median child: {statistics.median(durations):.3f}s")
        print(f"slowest:      {max(durations):.3f}s")
        print(f"straggler x:  {max(durations) / statistics.median(durations):.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunks", type=int, default=90)
    parser.add_argument("--concurrency", type=int, default=15)
    parser.add_argument("--failure-rate", type=float, default=0.05)
    parser.add_argument("--max-retries", type=int, default=2)
    asyncio.run(main(parser.parse_args()))
