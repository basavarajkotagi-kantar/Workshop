import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "app.db"

def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            watt INTEGER NOT NULL,
            priority INTEGER NOT NULL,
            status TEXT NOT NULL,
            userInput TEXT NOT NULL
        )
        """
    )
    existing_columns = {row["name"] for row in connection.execute("PRAGMA table_info(items)")}
    if "userInput" not in existing_columns:
        connection.execute("ALTER TABLE items ADD COLUMN userInput TEXT DEFAULT 'off'")
    connection.commit()
    return connection


class Database:
    """Async-style wrapper over the sync sqlite3 connection for use by routers."""

    async def fetch_all(self, query: str, params: dict | None = None) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(query, params or {}).fetchall()
        return [dict(row) for row in rows]

    async def fetch_one(self, query: str, params: dict | None = None) -> dict | None:
        with get_connection() as connection:
            row = connection.execute(query, params or {}).fetchone()
        return dict(row) if row else None
    

