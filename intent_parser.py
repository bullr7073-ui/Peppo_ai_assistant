import re
from datetime import datetime

# ==========================================
# HELPERS
# ==========================================

def clean_text(text):

    return re.sub(
        r"\s+",
        " ",
        text.lower().strip()
    )


def contains_any(text, phrases):

    return any(
        phrase in text
        for phrase in phrases
    )


# ==========================================
# APP NAME EXTRACTION
# ==========================================

APP_ALIASES = {

    "google chrome": "chrome",
    "chrome": "chrome",

    "visual studio code": "vs code",
    "vs code": "vs code",
    "code": "vs code",

    "notepad": "notepad",

    "calculator": "calculator",

    "spotify": "spotify",

    "vlc": "vlc",

    "file explorer": "explorer",
    "windows explorer": "explorer",
    "explorer": "explorer"
}


def extract_app(text):

    # Longest names first
    aliases = sorted(
        APP_ALIASES.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for name, app in aliases:

        if name in text:

            return app

    return None


# ==========================================
# BIRTHDAY VALUE EXTRACTION
# ==========================================

MONTHS = (
    "january|february|march|april|may|june|"
    "july|august|september|october|november|december"
)


def extract_birthday(text):

    pattern = (
        rf"\b({MONTHS})\s+"
        r"(\d{1,2})(?:st|nd|rd|th)?"
        r"(?:\s+(\d{4}))?\b"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:

        month = match.group(1)
        day = match.group(2)
        year = match.group(3)

        if year:

            return (
                f"{month.capitalize()} "
                f"{day} "
                f"{year}"
            )

        return (
            f"{month.capitalize()} "
            f"{day}"
        )

    return None


# ==========================================
# EVENT DATE
# ==========================================

def extract_date(text):

    date_phrases = [

        "day after tomorrow",
        "tomorrow",
        "today",

        "next monday",
        "next tuesday",
        "next wednesday",
        "next thursday",
        "next friday",
        "next saturday",
        "next sunday"

    ]

    for phrase in date_phrases:

        if phrase in text:

            return phrase

    return None


# ==========================================
# EVENT TITLE
# ==========================================

def extract_event_title(text):

    prefixes = [

        "i have ",
        "i need to ",
        "i need ",
        "i am going to ",
        "i'm going to ",
        "i want to ",
        "schedule ",
        "create an event for ",
        "create event for "

    ]

    title = text

    for prefix in prefixes:

        if title.startswith(prefix):

            title = title[len(prefix):]

            break

    # Remove date information
    for date_phrase in [

        "day after tomorrow",
        "tomorrow",
        "today"

    ]:

        title = title.replace(
            date_phrase,
            ""
        )

    title = re.sub(
        r"\s+",
        " ",
        title
    ).strip()

    return title


# ==========================================
# EVENT QUERY
# ==========================================

def extract_event_query(text):

    patterns = [

        r"my (.+?) appointment",
        r"my (.+?) meeting",
        r"my (.+?) event",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            return (
                match.group(1).strip()
                +
                (
                    " appointment"
                    if "appointment" in pattern
                    else
                    " meeting"
                    if "meeting" in pattern
                    else
                    " event"
                )
            )

    # Generic fallback
    for prefix in [

        "change my ",
        "move my ",
        "delete my ",
        "cancel my ",
        "reschedule my "

    ]:

        if text.startswith(prefix):

            query = text[len(prefix):]

            for date_phrase in [

                "day after tomorrow",
                "tomorrow",
                "today"

            ]:

                query = query.replace(
                    date_phrase,
                    ""
                )

            return query.strip()

    return None


# ==========================================
# MEMORY CONTENT
# ==========================================

def extract_memory_content(text):

    prefixes = [

        "remember that ",
        "remember ",
        "save that ",
        "save ",
        "don't forget that ",
        "dont forget that "

    ]

    for prefix in prefixes:

        if text.startswith(prefix):

            content = text[len(prefix):].strip()

            return content

    return None


# ==========================================
# FORGET MEMORY CONTENT
# ==========================================

def extract_forget_content(text):

    prefixes = [

        "forget that ",
        "forget "

    ]

    for prefix in prefixes:

        if text.startswith(prefix):

            content = text[len(prefix):].strip()

            return content

    return None


# ==========================================
# WEB SEARCH QUERY EXTRACTION
# ==========================================

def extract_web_query(text):

    prefixes = [

        "search the web for ",
        "search the web ",
        "search for ",
        "search ",
        "look up ",
        "look for ",
        "find information about ",
        "find information on ",
        "find out about ",
        "tell me about ",
        "give me information about ",
        "give me information on "

    ]

    for prefix in prefixes:

        if text.startswith(prefix):

            query = text[len(prefix):].strip()

            if query:

                return query

    return text.strip()


# ==========================================
# WEB SEARCH DETECTION
# ==========================================

def is_web_search(text):

    web_phrases = [

        "search the web",
        "search for",
        "search ",
        "look up",
        "look for",
        "find information about",
        "find information on",
        "find out about"

    ]

    return contains_any(
        text,
        web_phrases
    )


# ==========================================
# CURRENT / EXTERNAL INFORMATION DETECTION
# ==========================================

def needs_web_information(text):

    current_phrases = [

        "latest",
        "current",
        "today's",
        "todays",
        "recent",
        "news",
        "price",
        "prices",
        "release date",
        "released",
        "version",
        "weather",
        "stock price",
        "exchange rate"

    ]

    return contains_any(
        text,
        current_phrases
    )


# ==========================================
# PARSE USER INTENT
# ==========================================

def parse_intent(user_text):

    text = clean_text(
        user_text
    )


    # ======================================
    # EMPTY INPUT
    # ======================================

    if not text:

        return {
            "intent": "normal_chat"
        }


    # ======================================
    # BIRTHDAY
    # ======================================

    birthday_value = extract_birthday(
        text
    )


    # --------------------------------------
    # FORGET BIRTHDAY
    # --------------------------------------

    if (
        "forget my birthday" in text
        or
        "delete my birthday" in text
    ):

        return {
            "intent": "forget_birthday"
        }


    # --------------------------------------
    # RECALL BIRTHDAY
    # --------------------------------------

    if contains_any(
        text,
        [

            "when is my birthday",
            "what is my birthday",
            "tell me my birthday",
            "what's my birthday",
            "whats my birthday"

        ]
    ):

        return {
            "intent": "recall_birthday"
        }


    # --------------------------------------
    # UPDATE BIRTHDAY
    # --------------------------------------

    if (
        birthday_value
        and
        contains_any(
            text,
            [

                "update my birthday",
                "change my birthday",
                "modify my birthday"

            ]
        )
    ):

        return {
            "intent": "update_birthday",
            "value": birthday_value
        }


    # --------------------------------------
    # CREATE BIRTHDAY
    # --------------------------------------

    if birthday_value:

        if contains_any(
            text,
            [

                "my birthday is",
                "remember my birthday",
                "save my birthday",
                "birthday is"

            ]
        ):

            return {
                "intent": "create_birthday",
                "value": birthday_value
            }


    # ======================================
    # APP CONTROL
    # ======================================

    app = extract_app(
        text
    )


    # --------------------------------------
    # CHECK APP
    # --------------------------------------

    if (
        app
        and
        (
            "is " in text
            or
            "are " in text
        )
        and
        contains_any(
            text,
            [

                "running",
                "open"

            ]
        )
    ):

        return {
            "intent": "check_app",
            "app": app
        }


    # --------------------------------------
    # CLOSE APP
    # --------------------------------------

    if (
        app
        and
        contains_any(
            text,
            [

                "close ",
                "quit ",
                "exit ",
                "shut "

            ]
        )
    ):

        return {
            "intent": "close_app",
            "app": app
        }


    # --------------------------------------
    # OPEN APP
    # --------------------------------------

    if (
        app
        and
        contains_any(
            text,
            [

                "open ",
                "launch ",
                "start ",
                "run "

            ]
        )
    ):

        return {
            "intent": "open_app",
            "app": app
        }


    # ======================================
    # MEMORY
    # ======================================

    # --------------------------------------
    # FORGET MEMORY
    # --------------------------------------

    if contains_any(
        text,
        [

            "forget that ",
            "forget "

        ]
    ):

        # Don't catch birthday
        if "birthday" not in text:

            content = extract_forget_content(
                text
            )

            if content:

                return {
                    "intent": "forget_memory",
                    "content": content
                }


    # --------------------------------------
    # CREATE MEMORY
    # --------------------------------------

    if contains_any(
        text,
        [

            "remember that ",
            "remember ",
            "save that ",
            "save "

        ]
    ):

        # Don't catch birthday
        if "birthday" not in text:

            content = extract_memory_content(
                text
            )

            if content:

                return {
                    "intent": "create_memory",
                    "content": content
                }


    # ======================================
    # EVENTS
    # ======================================

    event_date = extract_date(
        text
    )


    # --------------------------------------
    # DELETE EVENT
    # --------------------------------------

    if contains_any(
        text,
        [

            "delete my ",
            "cancel my "

        ]
    ):

        event_query = extract_event_query(
            text
        )

        if event_query:

            return {
                "intent": "delete_event",
                "event_query": event_query
            }


    # --------------------------------------
    # UPDATE EVENT
    # --------------------------------------

    if (
        event_date
        and
        contains_any(
            text,
            [

                "move my ",
                "change my ",
                "reschedule my "

            ]
        )
    ):

        event_query = extract_event_query(
            text
        )

        if event_query:

            return {
                "intent": "update_event",
                "event_query": event_query,
                "date": event_date
            }


    # --------------------------------------
    # RECALL EVENT
    # --------------------------------------

    if (
        event_date
        and
        contains_any(
            text,
            [

                "what do i have",
                "what do i have planned",
                "what is happening",
                "what's happening",
                "what's on my calendar",
                "whats on my calendar"

            ]
        )
    ):

        return {
            "intent": "recall_event",
            "date": event_date
        }


    # --------------------------------------
    # CREATE EVENT
    # --------------------------------------

    if (
        event_date
        and
        contains_any(
            text,
            [

                "i have ",
                "i need to ",
                "i need ",
                "i am going to ",
                "i'm going to ",
                "schedule ",
                "create an event"

            ]
        )
    ):

        title = extract_event_title(
            text
        )

        if title:

            return {
                "intent": "create_event",
                "title": title,
                "date": event_date
            }


    # ======================================
    # WEB SEARCH
    # ======================================

    # Explicit web search
    if is_web_search(
        text
    ):

        query = extract_web_query(
            text
        )

        if query:

            return {
                "intent": "web_search",
                "query": query
            }


    # --------------------------------------
    # CURRENT INFORMATION
    # --------------------------------------

    if needs_web_information(
        text
    ):

        return {
            "intent": "web_search",
            "query": text
        }


    # ======================================
    # NORMAL CHAT
    # ======================================

    return {
        "intent": "normal_chat"
    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print(
        "Peppo Local Intent Router Test"
    )

    print(
        "=============================="
    )


    tests = [

        # ------------------------------
        # NORMAL CHAT
        # ------------------------------

        "How are you?",

        "What do you think about AI?",


        # ------------------------------
        # MEMORY
        # ------------------------------

        "remember that I like Formula 1",

        "remember that I enjoy technology",

        "forget that I like Formula 1",


        # ------------------------------
        # BIRTHDAY
        # ------------------------------

        "my birthday is November 7 2005",

        "remember my birthday is November 7 2005",

        "when is my birthday?",

        "tell me my birthday",

        "update my birthday to November 9 2005",


        # ------------------------------
        # EVENTS
        # ------------------------------

        "I have a dentist appointment tomorrow",

        "Move my dentist appointment to day after tomorrow",

        "What do I have tomorrow?",

        "delete my dentist appointment",

        "cancel my meeting",


        # ------------------------------
        # APP CONTROL
        # ------------------------------

        "Open Chrome",

        "Launch Google Chrome",

        "Open VS Code",

        "Open calculator",

        "Close Chrome",

        "Close VS Code",

        "Quit Notepad",

        "Is Chrome running?",

        "Is Chrome open?",

        "Is VS Code running?",

        "Is Notepad open?",


        # ------------------------------
        # WEB SEARCH
        # ------------------------------

        "Search the web for Raspberry Pi 5",

        "Search for Python programming",

        "Look up Mojo programming language",

        "Tell me about Nikola Tesla",

        "Find information about quantum computing",

        "What is the latest version of Python?",

        "What is the current price of Bitcoin?",

        "What are the latest AI news?",

        "What is the weather today?"

    ]


    for test in tests:

        print(
            f"\nYou: {test}"
        )

        result = parse_intent(
            test
        )

        print(
            "Intent:",
            result
        )