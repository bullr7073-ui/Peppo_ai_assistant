from database import delete_event

if delete_event(6):
    print("Duplicate event deleted successfully.")
else:
    print("Event not found.")