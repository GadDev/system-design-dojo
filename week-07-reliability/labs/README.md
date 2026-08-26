# Week 7 Labs

These labs are intentionally small and framework-light. They exist to make reliability behavior visible.

## 1. `retry_backoff_simulator.py`

Simulates many clients retrying a failing dependency.

Compare:

```bash
python retry_backoff_simulator.py --clients 200 --jitter none
python retry_backoff_simulator.py --clients 200 --jitter full
```

Observe how jitter spreads retry traffic.

## 2. `circuit_breaker_demo.py`

Tiny CLOSED / OPEN / HALF_OPEN circuit-breaker simulator.

```bash
python circuit_breaker_demo.py
```

The implementation is educational, not production-grade.

## 3. `fault_injection_simulator.py`

Runs a toy transcription chunk workflow with injected:

- AI 429,
- R2 503,
- worker crash after durable output,
- PostgreSQL unavailable.

```bash
python fault_injection_simulator.py --scenario worker-crash
python fault_injection_simulator.py --scenario ai-429
python fault_injection_simulator.py --scenario r2-503
python fault_injection_simulator.py --scenario db-down
```

## 4. `health_check_example.py`

Minimal FastAPI example separating:

```text
/livez
/readyz
```

Run if FastAPI is installed:

```bash
uvicorn health_check_example:app --reload
```

Use it to discuss what should and should not make a process unready/unlive.
