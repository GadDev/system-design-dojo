# Lab — FastAPI Behind NGINX

## Goal

See horizontal request distribution rather than only drawing it.

Architecture:

```text
curl
 ↓
NGINX :8080
 ├── api1:8000
 ├── api2:8000
 └── api3:8000
```

---

# Run

From this directory:

```bash
docker compose up --build
```

Then:

```bash
for i in {1..12}; do curl -s http://localhost:8080/instance; echo; done
```

You should observe different host/container identifiers.

---

# Kill a replica

```bash
docker compose stop api2
```

Repeat requests.

Questions:

1. Does traffic continue?
2. What errors appear while NGINX learns the backend is unavailable?
3. How would active health checks/readiness improve this in a production environment?

---

# Change policy

Open `nginx.conf`.

Add:

```nginx
least_conn;
```

inside the `upstream` block.

Rebuild/restart and compare.

---

# Slow-request experiment

Run several slow requests:

```bash
curl 'http://localhost:8080/slow?seconds=3'
```

in parallel while calling `/instance`.

Observe why active connection count can matter when request durations vary.

---

# Cleanup

```bash
docker compose down
```

---

# Reflection

Write:

```text
What did the load balancer know?
What did it not know?
What state would break if stored only inside one replica?
What shared dependency did this lab omit?
```

---

# Optional load test with k6

If you have `k6` installed:

```bash
k6 run load_test.js
```

The script ramps virtual users and checks:

```text
failure rate < 1%
p95 < 500 ms
```

Those thresholds are **lab values**, not production SLOs.

While it runs, change the lab deliberately:

1. stop one API replica,
2. call the `/slow` endpoint instead,
3. compare round robin vs least-connections,
4. observe when latency rises before errors appear.

The goal is to connect:

```text
offered load → saturation → latency → errors
```
