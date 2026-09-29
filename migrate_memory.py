import json
import os

from database import (
    initialize_database,
    set_personal,
    add_memory,
    add_event
)


MEMORY_FILE = "memory.json"


# ==========================================
# MIGRATE JSON → SQLITE
# ==========================================

def migrate_memory():

    if not os.path.exists(MEMORY_FILE):

        print("memory.json was not found.")

        return


    # Initialize database
    initialize_database()


    # Load JSON
    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            memory = json.load(file)

    except Exception as error:

        print(
            "Could not read memory.json:",
            error
        )

        return


    # ==========================================
    # PERSONAL INFORMATION
    # ==========================================

    personal = memory.get(
        "personal",
        {}
    )

    for key, value in personal.items():

        set_personal(
            key,
            str(value)
        )

        print(
            f"Personal → {key}: {value}"
        )


    # ==========================================
    # GENERAL MEMORIES
    # ==========================================

    memories = memory.get(
        "memories",
        []
    )

    for fact in memories:

        add_memory(
            str(fact)
        )

        print(
            f"Memory → {fact}"
        )


    # ==========================================
    # EVENTS
    # ==========================================

    events = memory.get(
        "events",
        []
    )

    for event in events:

        title = event.get(
            "title",
            ""
        )

        date = event.get(
            "date"
        )

        if title:

            add_event(
                title,
                date
            )

            print(
                f"Event → {title} → {date}"
            )


    print(
        "\nMigration completed successfully! 🎉"
    )


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    migrate_memory()