from datetime import datetime, timedelta

from memory import (
    remember_personal,
    recall_personal,
    forget_personal,
    remember_fact,
    forget_fact,
    remember_event,
    get_events_for_date,
)

from database import (
    get_events,
    delete_event,
)

from process_manager import (
    open_application,
    close_application,
    is_application_running,
)


# ==========================================
# DATE CONVERSION
# ==========================================

def resolve_date(date_text):

    if not date_text:
        return None

    text = date_text.lower().strip()

    today = datetime.now().date()

    if text == "today":

        return today.strftime("%Y-%m-%d")

    if text == "tomorrow":

        return (
            today + timedelta(days=1)
        ).strftime("%Y-%m-%d")

    if text == "day after tomorrow":

        return (
            today + timedelta(days=2)
        ).strftime("%Y-%m-%d")

    return date_text


# ==========================================
# HANDLE INTENT
# ==========================================

def handle_intent(intent_data):

    intent = intent_data.get("intent")


    # ======================================
    # CREATE BIRTHDAY
    # ======================================

    if intent == "create_birthday":

        value = intent_data.get("value")

        if not value:

            return (
                "I didn't catch your birthday."
            )

        remember_personal(
            "birthday",
            value
        )

        return (
            f"Got it. I'll remember your birthday "
            f"is {value}."
        )


    # ======================================
    # UPDATE BIRTHDAY
    # ======================================

    if intent == "update_birthday":

        value = intent_data.get("value")

        if not value:

            return (
                "I didn't catch the new birthday."
            )

        remember_personal(
            "birthday",
            value
        )

        return (
            f"Got it. I've updated your birthday "
            f"to {value}."
        )


    # ======================================
    # RECALL BIRTHDAY
    # ======================================

    if intent == "recall_birthday":

        birthday = recall_personal(
            "birthday"
        )

        if birthday:

            return (
                f"Your birthday is "
                f"{birthday}."
            )

        return (
            "I don't have your birthday "
            "saved yet."
        )


    # ======================================
    # FORGET BIRTHDAY
    # ======================================

    if intent == "forget_birthday":

        forgotten = forget_personal(
            "birthday"
        )

        if forgotten:

            return (
                "I've forgotten your birthday."
            )

        return (
            "I don't have your birthday "
            "saved."
        )


    # ======================================
    # CREATE MEMORY
    # ======================================

    if intent == "create_memory":

        content = intent_data.get(
            "content"
        )

        if not content:

            return (
                "I didn't catch what you want "
                "me to remember."
            )

        remember_fact(
            content
        )

        return (
            "Got it. I'll remember that."
        )


    # ======================================
    # FORGET MEMORY
    # ======================================

    if intent == "forget_memory":

        content = intent_data.get(
            "content"
        )

        if not content:

            return (
                "I didn't catch what you want "
                "me to forget."
            )

        if forget_fact(content):

            return (
                "I've forgotten that."
            )

        return (
            "I couldn't find that in my memory."
        )


    # ======================================
    # CREATE EVENT
    # ======================================

    if intent == "create_event":

        title = intent_data.get(
            "title"
        )

        date_text = intent_data.get(
            "date"
        )

        if not title:

            return (
                "I didn't catch what event "
                "you want me to remember."
            )

        event_date = resolve_date(
            date_text
        )

        remember_event(
            title,
            event_date
        )

        if event_date:

            return (
                f"Got it. I'll remember "
                f"{title} for {date_text}."
            )

        return (
            f"Got it. I'll remember "
            f"{title}."
        )


    # ======================================
    # RECALL EVENT
    # ======================================

    if intent == "recall_event":

        date_text = intent_data.get(
            "date"
        )

        event_date = resolve_date(
            date_text
        )

        if not event_date:

            return (
                "I need a date to check "
                "your schedule."
            )

        events = get_events_for_date(
            event_date
        )

        if not events:

            return (
                f"You don't have anything "
                f"scheduled for {date_text}."
            )

        if len(events) == 1:

            return (
                f"You have "
                f"{events[0]['title']} "
                f"on {date_text}."
            )

        titles = [
            event["title"]
            for event in events
        ]

        return (
            f"On {date_text}, you have "
            + ", ".join(titles)
            + "."
        )


    # ======================================
    # UPDATE EVENT
    # ======================================

    if intent == "update_event":

        event_query = intent_data.get(
            "event_query"
        )

        date_text = intent_data.get(
            "date"
        )

        if not event_query:

            return (
                "I need to know which event "
                "you want to move."
            )

        if not date_text:

            return (
                "I need to know the new date."
            )

        new_date = resolve_date(
            date_text
        )

        events = get_events()

        matching_event = None

        for event in events:

            title = event["title"].lower()

            if event_query.lower() in title:

                matching_event = event

                break

        if not matching_event:

            return (
                f"I couldn't find an event "
                f"called {event_query}."
            )


        # ==================================
        # UPDATE EVENT IN DATABASE
        # ==================================

        from database import get_connection

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE events
            SET event_date = ?
            WHERE id = ?
            """,
            (
                new_date,
                matching_event["id"]
            )
        )

        connection.commit()

        connection.close()

        return (
            f"Done. I've moved "
            f"{matching_event['title']} "
            f"to {date_text}."
        )


    # ======================================
    # DELETE EVENT
    # ======================================

    if intent == "delete_event":

        event_query = intent_data.get(
            "event_query"
        )

        if not event_query:

            return (
                "I need to know which event "
                "you want me to delete."
            )

        events = get_events()

        for event in events:

            if (
                event_query.lower()
                in event["title"].lower()
            ):

                delete_event(
                    event["id"]
                )

                return (
                    f"Done. I've removed "
                    f"{event['title']} "
                    f"from your schedule."
                )

        return (
            f"I couldn't find "
            f"{event_query} in your schedule."
        )


    # ======================================
    # OPEN APPLICATION
    # ======================================

    if intent == "open_app":

        app = intent_data.get(
            "app"
        )

        if not app:

            return (
                "I didn't catch which application "
                "you want me to open."
            )

        success, message = open_application(
            app
        )

        return message


    # ======================================
    # CLOSE APPLICATION
    # ======================================

    if intent == "close_app":

        app = intent_data.get(
            "app"
        )

        if not app:

            return (
                "I didn't catch which application "
                "you want me to close."
            )

        success, message = close_application(
            app
        )

        return message


    # ======================================
    # CHECK APPLICATION
    # ======================================

    if intent == "check_app":

        app = intent_data.get(
            "app"
        )

        if not app:

            return (
                "I didn't catch which application "
                "you want me to check."
            )

        running = is_application_running(
            app
        )

        if running:

            return (
                f"Yes, {app} is currently running."
            )

        return (
            f"No, {app} is not running."
        )


    # ======================================
    # NORMAL CHAT
    # ======================================

    if intent == "normal_chat":

        return None


    # ======================================
    # UNKNOWN INTENT
    # ======================================

    return None