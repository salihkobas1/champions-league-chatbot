import sqlite3
from app.core.config import SQLITE_DB_PATH


def get_db_connection():
    """
    Creates a SQLite database connection.
    This function should be used by services instead of calling sqlite3.connect directly.
    """
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn