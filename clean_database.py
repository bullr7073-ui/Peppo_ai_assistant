from database import (
    initialize_database,
    get_events,
    delete_event
)


initialize_database()


print("Current events:\n")

events = get_events()

for event in events:

    print(
        f"[{event['id']}] "
        f"{event['title']} "
        f"→ {event['event_date']}"
    )


print("\nRemoving incorrect question/event entries...\n")


for event in events:

    title = event["title"].lower()

    # Remove the old question-like entries
    if (
        "do i have tomorrow" in title
        or title == "tomorrow i have to go to the"
    ):

        delete_event(event["id"])

        print(
            f"Deleted: {event['title']}"
        )


print("\nRemaining events:\n")

events = get_events()

for event in events:

    print(
        f"[{event['id']}] "
        f"{event['title']} "
        f"→ {event['event_date']}"
    )


print("\nDatabase cleanup complete! ✅")