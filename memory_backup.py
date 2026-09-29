import json
import os
from datetime import datetime, timedelta


MEMORY_FILE = "memory.json"


# ==========================================
# DEFAULT MEMORY
# ==========================================

DEFAULT_MEMORY = {
    "personal": {},
    "memories": [],
    "events": []
}


# ==========================================
# LOAD MEMORY
# ==========================================

def load_memory():

    if not os.path.exists(MEMORY_FILE):

        save_memory(DEFAULT_MEMORY.copy())

        return DEFAULT_MEMORY.copy()

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            memory = json.load(file)

    except (json.JSONDecodeError, OSError):

        memory = DEFAULT_MEMORY.copy()


    memory.setdefault("personal", {})
    memory.setdefault("memories", [])
    memory.setdefault("events", [])

    return memory


# ==========================================
# SAVE MEMORY
# ==========================================

def save_memory(memory):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# PERSONAL MEMORY
# ==========================================

def remember_personal(key, value):

    memory = load_memory()

    memory["personal"][key] = value

    save_memory(memory)

    return True


def recall_personal(key):

    memory = load_memory()

    return memory["personal"].get(key)


def forget_personal(key):

    memory = load_memory()

    if key in memory["personal"]:

        del memory["personal"][key]

        save_memory(memory)

        return True

    return False


# ==========================================
# GENERAL MEMORIES
# ==========================================

def remember_fact(fact):

    memory = load_memory()

    if fact not in memory["memories"]:

        memory["memories"].append(fact)

        save_memory(memory)

    return True


def get_memories():

    memory = load_memory()

    return memory["memories"]


def forget_fact(fact):

    memory = load_memory()

    original_count = len(
        memory["memories"]
    )

    memory["memories"] = [
        item
        for item in memory["memories"]
        if item.lower() != fact.lower()
    ]

    save_memory(memory)

    return len(memory["memories"]) < original_count


# ==========================================
# EVENTS
# ==========================================

def remember_event(title, date=None):

    memory = load_memory()

    event = {
        "title": title,
        "date": date
    }

    memory["events"].append(event)

    save_memory(memory)

    return True


# ==========================================
# CLEAN EXPIRED EVENTS
# ==========================================

def cleanup_expired_events():

    memory = load_memory()

    today = datetime.now().date()

    active_events = []

    for event in memory["events"]:

        event_date = event.get("date")

        # Keep events without a date for now
        if not event_date:

            active_events.append(event)

            continue

        try:

            event_day = datetime.strptime(
                event_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            active_events.append(event)

            continue


        # Keep today and future events
        if event_day >= today:

            active_events.append(event)


    memory["events"] = active_events

    save_memory(memory)

    return active_events


# ==========================================
# GET EVENTS
# ==========================================

def get_events():

    cleanup_expired_events()

    memory = load_memory()

    return memory["events"]


# ==========================================
# FORGET EVENT
# ==========================================

def forget_event(title):

    memory = load_memory()

    original_count = len(
        memory["events"]
    )

    memory["events"] = [
        event
        for event in memory["events"]
        if event.get("title", "").lower()
        != title.lower()
    ]

    save_memory(memory)

    return len(memory["events"]) < original_count


# ==========================================
# DATE HELPERS
# ==========================================

def today_date():

    return datetime.now().strftime(
        "%Y-%m-%d"
    )


def tomorrow_date():

    tomorrow = (
        datetime.now()
        + timedelta(days=1)
    )

    return tomorrow.strftime(
        "%Y-%m-%d"
    )