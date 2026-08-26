import time

primary = {"status": "PROCESSING", "version": 10, "progress": 73}
replica = primary.copy()

print("initial", "primary=", primary, "replica=", replica)

# Mutation commits on the primary and the API returns the new representation.
primary = {"status": "COMPLETED", "version": 11, "progress": 100}
client_shown = primary.copy()
print("\nwrite committed on primary; client now knows:", client_shown)

# An immediate read is accidentally routed to a lagging replica.
received = replica
print("immediate stale replica read:", received)

# UI-level monotonic protection: never move an already observed version/progress backward.
if received["version"] >= client_shown["version"]:
    client_shown = received.copy()
print("client monotonic display remains:", client_shown)

print("\n...replication catches up...")
time.sleep(0.1)
replica = primary.copy()
print("replica:", replica)

print("\nLesson: monotonic display protects UX, but authoritative mutation decisions still need an authoritative read/write contract.")
