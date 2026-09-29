from database import get_events_by_date
from memory import tomorrow_date

events = get_events_by_date(tomorrow_date())

print(f"Events on {tomorrow_date()}:\n")

for event in events:
    print(
        f"- ID {event['id']}: "
        f"{event['title']} → "
        f"{event['event_date']}"
    )