from memory import (
    get_events_for_date,
    tomorrow_date
)


tomorrow = tomorrow_date()

print(
    f"\nEvents for {tomorrow}:\n"
)


events = get_events_for_date(
    tomorrow
)


if not events:

    print(
        "No events scheduled."
    )

else:

    for event in events:

        print(
            f"- {event['title']}"
        )