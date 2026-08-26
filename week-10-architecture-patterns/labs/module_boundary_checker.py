"""Tiny architecture fitness-function demo.

We model allowed module dependencies and check sample imports. In a real repository,
you could walk Python ASTs and fail CI when a module imports another module's
private implementation package.
"""

ALLOWED = {
    "identity": set(),
    "uploads": {"identity"},
    "jobs": {"identity", "uploads"},
    "results": {"jobs"},
    "billing": {"jobs"},
    "notifications": {"jobs"},
}

IMPORTS = [
    ("uploads", "identity", "public"),
    ("jobs", "uploads", "public"),
    ("billing", "jobs", "public"),
    ("billing", "jobs", "repository"),  # private internals: violation
    ("jobs", "billing", "public"),      # dependency direction: violation
]


def check_import(source: str, target: str, surface: str) -> tuple[bool, str]:
    if target not in ALLOWED[source]:
        return False, f"{source} is not allowed to depend on {target}"
    if surface != "public":
        return False, f"{source} imports private {target}.{surface}"
    return True, "allowed"


def main() -> None:
    violations = 0
    for source, target, surface in IMPORTS:
        ok, reason = check_import(source, target, surface)
        status = "OK" if ok else "VIOLATION"
        print(f"{status:9} {source:14} -> {target}.{surface:10} | {reason}")
        violations += int(not ok)

    print(f"\nviolations={violations}")
    if violations:
        print("In CI, this would fail the architecture fitness function.")


if __name__ == "__main__":
    main()
