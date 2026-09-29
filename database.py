from datetime import datetime
import sqlite3


DATABASE_FILE = "peppo.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    connection = sqlite3.connect(DATABASE_FILE)

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================
# CREATE TABLES
# ==========================================

def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            event_date TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ==========================================
# ADD MEMORY
# ==========================================

def add_memory(content):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO memories (content, created_at)
        VALUES (?, ?)
    """, (
        content,
        datetime.now().isoformat()
    ))

    connection.commit()
    connection.close()


# ==========================================
# GET MEMORIES
# ==========================================

def get_memories():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, content, created_at
        FROM memories
        ORDER BY id DESC
    """)

    memories = cursor.fetchall()

    connection.close()

    return memories


# ==========================================
# DELETE MEMORY
# ==========================================

def delete_memory(memory_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM memories
        WHERE id = ?
    """, (memory_id,))

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted


# ==========================================
# TEST DATABASE
# ==========================================

# ==========================================
# PERSONAL INFORMATION
# ==========================================

def set_personal(key, value):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO personal (key, value)
        VALUES (?, ?)
        ON CONFLICT(key)
        DO UPDATE SET value = excluded.value
    """, (key, value))

    connection.commit()
    connection.close()

# ==========================================
# UPDATE PERSONAL INFORMATION
# ==========================================

def update_personal(key, value):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE personal
        SET value = ?
        WHERE key = ?
    """, (value, key))

    updated = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return updated


def get_personal(key):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT value
        FROM personal
        WHERE key = ?
    """, (key,))

    result = cursor.fetchone()

    connection.close()

    if result:
        return result["value"]

    return None


def delete_personal(key):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM personal
        WHERE key = ?
    """, (key,))

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted


# ==========================================
# EVENTS
# ==========================================

def add_event(title, event_date):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO events (
            title,
            event_date,
            created_at
        )
        VALUES (?, ?, ?)
    """, (
        title,
        event_date,
        datetime.now().isoformat()
    ))

    connection.commit()
    connection.close()


def get_events():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, event_date, created_at
        FROM events
        ORDER BY event_date ASC
    """)

    events = cursor.fetchall()

    connection.close()

    return events


def delete_event(event_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM events
        WHERE id = ?
    """, (event_id,))

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted


# ==========================================
# DATABASE TEST
# ==========================================

if __name__ == "__main__":

    initialize_database()

    print("Peppo database initialized successfully.")



def get_events_by_date(event_date):

    conn = sqlite3.connect(DATABASE_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, event_date
        FROM events
        WHERE event_date = ?
        ORDER BY id ASC
        """,
        (event_date,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "event_date": row[2]
        }
        for row in rows
    ]
