"""SQLite database helpers — Phase 1 will populate this."""
import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.environ.get("RAILWAY_DATABASE_PATH", "data/portal.db")


@contextmanager
def get_connection():
    """Context-managed SQLite connection with WAL mode for Railway."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Initialize schema — to be implemented in Phase 1."""
    pass
