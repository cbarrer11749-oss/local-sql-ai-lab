import sqlite3


_ALLOWED_COLUMNS = {"name": "name", "id": "id"}


def search_by_column(db: sqlite3.Connection, requested_column: str, name: str):
    """Select a known column; bind the external value as data."""
    column = _ALLOWED_COLUMNS.get(requested_column)
    if column is None:
        raise ValueError("Unknown column")
    return db.execute(
        f"SELECT {column} FROM users WHERE name = ?", (name,)
    ).fetchall()


def find_by_name(db: sqlite3.Connection, name: str):
    """Find an exact name without interpolating it into SQL syntax."""
    return db.execute("SELECT id FROM users WHERE name = ?", (name,)).fetchall()


def find_by_id(db: sqlite3.Connection, raw_id: str):
    """Accept an integer ID and bind it as a SQL value."""
    try:
        user_id = int(raw_id)
    except (TypeError, ValueError) as exc:
        raise ValueError("ID must be an integer") from exc
    return db.execute(
        "SELECT name FROM users WHERE id = ?", (user_id,)
    ).fetchall()
