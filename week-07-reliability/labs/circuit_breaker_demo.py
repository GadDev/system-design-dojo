#!/usr/bin/env python3
from collections import deque


class CircuitBreaker:
    def __init__(self, window=5, failure_threshold=0.6, open_for_ticks=3, half_open_calls=2):
        self.window = window
        self.failure_threshold = failure_threshold
        self.open_for_ticks = open_for_ticks
        self.half_open_calls = half_open_calls
        self.results = deque(maxlen=window)
        self.state = "CLOSED"
        self.opened_at = None
        self.half_open_used = 0

    def allow(self, tick):
        if self.state == "OPEN" and tick - self.opened_at >= self.open_for_ticks:
            self.state = "HALF_OPEN"
            self.half_open_used = 0
        if self.state == "OPEN":
            return False
        if self.state == "HALF_OPEN" and self.half_open_used >= self.half_open_calls:
            return False
        if self.state == "HALF_OPEN":
            self.half_open_used += 1
        return True

    def record(self, success, tick):
        if self.state == "HALF_OPEN":
            if not success:
                self.state = "OPEN"
                self.opened_at = tick
                return
            if self.half_open_used >= self.half_open_calls:
                self.state = "CLOSED"
                self.results.clear()
                return

        if self.state == "CLOSED":
            self.results.append(success)
            if len(self.results) == self.window:
                failures = sum(not x for x in self.results)
                if failures / self.window >= self.failure_threshold:
                    self.state = "OPEN"
                    self.opened_at = tick


def main():
    dependency_outcomes = [True, False, False, False, False, True, True, True, True, True, True]
    cb = CircuitBreaker()
    for tick, outcome in enumerate(dependency_outcomes):
        if not cb.allow(tick):
            print(f"tick={tick:02d} state={cb.state:<9} call=BLOCKED")
            continue
        print(f"tick={tick:02d} state={cb.state:<9} call={'OK' if outcome else 'FAIL'}")
        cb.record(outcome, tick)
    print("final state:", cb.state)


if __name__ == "__main__":
    main()
