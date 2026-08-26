from dataclasses import dataclass, field


@dataclass
class State:
    job_created: bool = False
    quota_reserved: bool = False
    processed: bool = False
    billed: bool = False
    events: list[str] = field(default_factory=list)


state = State()


def do(name, action):
    print("DO ", name)
    action()
    state.events.append(name)


def compensate(name, action):
    print("UNDO", name)
    action()
    state.events.append("compensate:" + name)


try:
    do("create-job", lambda: setattr(state, "job_created", True))
    do("reserve-quota", lambda: setattr(state, "quota_reserved", True))
    do("process-video", lambda: setattr(state, "processed", True))

    print("DO  charge-usage")
    raise RuntimeError("billing service unavailable")
except Exception as exc:
    print("FAIL", exc)
    # Business-specific compensation; expensive processing cannot be 'uncomputed'.
    if state.quota_reserved:
        compensate("reserve-quota", lambda: setattr(state, "quota_reserved", False))
    # Keep processed artifact for TTL/retry; mark workflow billing-pending in a real system.

print("\nstate:", state)
print("Lesson: compensation reaches an acceptable business state; it is not time travel.")
