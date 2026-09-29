from datetime import datetime, timedelta

from database import (
    initialize_database,
    set_personal,
    get_personal,
    delete_personal,
    add_memory,
    get_memories as database_get_memories,
    delete_memory,
    add_event,
    get_events as database_get_events,
    delete_event
)




# ==========================================
# INITIALIZE DATABASE
# ==========================================

initialize_database()


# ==========================================
# PERSONAL MEMORY
# ==========================================

def remember_personal(key, value):

    set_personal(key, value)

    return True


def recall_personal(key):

    return get_personal(key)


def forget_personal(key):

    return delete_personal(key)


# ==========================================
# GENERAL MEMORIES
# ==========================================

def remember_fact(fact):

    memories = database_get_memories()

    for memory in memories:

        if memory["content"].lower() == fact.lower():

            return True

    add_memory(fact)

    return True


def get_memories():

    memories = database_get_memories()

    return [
        memory["content"]
        for memory in memories
    ]


def forget_fact(fact):

    memories = database_get_memories()

    forgotten = False

    for memory in memories:

        if memory["content"].lower() == fact.lower():

            if delete_memory(memory["id"]):

                forgotten = True

    return forgotten


# ==========================================
# EVENTS
# ==========================================

from database import (
    add_event,
    get_events as db_get_events,
    get_events_by_date,
    delete_event
)


def remember_event(title, date=None):

    add_event(
        title,
        date
    )

    return True


def get_events():

    return db_get_events()


def get_events_for_date(event_date):

    return get_events_by_date(
        event_date
    )


def forget_event(title):

    events = db_get_events()

    deleted = False

    for event in events:

        if event["title"].lower() == title.lower():

            if delete_event(event["id"]):

                deleted = True

    return deleted

# ==========================================
# CLEAN EXPIRED EVENTS
# ==========================================

def cleanup_expired_events():

    events = database_get_events()

    today = datetime.now().date()

    active_events = []

    for event in events:

        event_date = event["event_date"]

        # Keep events without dates
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

        # Delete expired events
        if event_day < today:

            delete_event(
                event["id"]
            )

        else:

            active_events.append(event)

    return active_events


# ==========================================
# GET EVENTS
# ==========================================

def get_events():

    return cleanup_expired_events()


# ==========================================
# FORGET EVENT
# ==========================================

def forget_event(title):

    events = database_get_events()

    forgotten = False

    for event in events:

        if (
            event["title"].lower()
            == title.lower()
        ):

            if delete_event(event["id"]):

                forgotten = True

    return forgotten


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


# ==========================================
# NATURAL EVENT RESPONSE
# ==========================================

def get_event_response(event_date):

    events = get_events_for_date(event_date)

    if not events:

        return None

    if len(events) == 1:

        return events[0]["title"]

    titles = [
        event["title"]
        for event in events
    ]

    return ", ".join(titles)


from database import update_personal
# ==========================================
# UPDATE PERSONAL MEMORY
# ==========================================

def update_personal_memory(key, value):

    return update_personal(
        key,
        value
    )