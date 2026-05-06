"""Seed database with the Smith Family sample client — Phase 1 will populate."""
from database import init_db, get_connection


def seed():
    """Load Smith Family sample data — Phase 1 implementation."""
    init_db()
    pass


if __name__ == "__main__":
    seed()
    print("Seed complete.")
