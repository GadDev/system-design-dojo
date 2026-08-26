try:
    from fastapi import FastAPI, Response
except ImportError as exc:
    raise SystemExit("Install FastAPI first: pip install fastapi uvicorn") from exc

app = FastAPI()

# Educational toggles. In production these would come from real state.
db_ready = True
draining = False


@app.get("/livez")
def livez():
    # Keep liveness cheap and focused on whether restarting THIS process may help.
    return {"status": "alive"}


@app.get("/readyz")
def readyz(response: Response):
    # Readiness answers whether this instance should receive normal traffic now.
    if draining or not db_ready:
        response.status_code = 503
        return {"status": "not-ready", "db_ready": db_ready, "draining": draining}
    return {"status": "ready"}
