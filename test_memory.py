from memory import (
    remember_personal,
    recall_personal,
    forget_personal,
    remember_fact,
    get_memories,
    forget_fact,
    remember_event,
    get_events,
    forget_event
)


print("\n========== PERSONAL ==========")

remember_personal(
    "test_name",
    "Peppo Developer"
)

print(
    "Stored:",
    recall_personal("test_name")
)


print("\n========== GENERAL MEMORY ==========")

remember_fact(
    "I love Formula 1."
)

print("Memories:")

for memory in get_memories():

    print("-", memory)


print("\n========== FORGET MEMORY ==========")

result = forget_fact(
    "I love Formula 1."
)

print(
    "Forgot:",
    result
)


print("\n========== EVENTS ==========")

remember_event(
    "Dentist appointment",
    "2026-08-22"
)

print("Events:")

for event in get_events():

    print(
        "-",
        event["title"],
        "→",
        event["event_date"]
    )


print("\n========== FORGET EVENT ==========")

result = forget_event(
    "Dentist appointment"
)

print(
    "Forgot event:",
    result
)


print("\n========== PERSONAL DELETE ==========")

result = forget_personal(
    "test_name"
)

print(
    "Forgot personal info:",
    result
)