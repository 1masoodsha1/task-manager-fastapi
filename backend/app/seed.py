from datetime import datetime, timedelta, timezone

from .database import get_connection


def create_tables() -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NULL,
            status TEXT NOT NULL DEFAULT 'TODO',
            due_date TEXT NULL
        )
    """)

    conn.commit()
    conn.close()


def seed_tasks() -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM tasks")
    count = cur.fetchone()[0]

    if count == 0:
        now = datetime.now(timezone.utc)
        rows = [
            ("Buy groceries", "Milk, eggs, bread, fruit, and rice.", "TODO", (now + timedelta(days=1)).isoformat()),
            ("Do laundry", "Wash clothes and fold them in the evening.", "IN_PROGRESS", (now + timedelta(hours=8)).isoformat()),
            ("Clean the room", "Vacuum the floor and organize the desk.", "TODO", (now + timedelta(days=2)).isoformat()),
            ("Pay electricity bill", "Check the online account and make the payment.", "TODO", (now + timedelta(days=3)).isoformat()),
        ]

        cur.executemany(
            "INSERT INTO tasks (title, description, status, due_date) VALUES (?, ?, ?, ?)",
            rows,
        )
        conn.commit()

    conn.close()