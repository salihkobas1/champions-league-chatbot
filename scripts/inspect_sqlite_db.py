import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.core.config import SQLITE_DB_PATH
from app.core.database import get_db_connection


def inspect_database():
    if not SQLITE_DB_PATH.exists():
        print(f"Database not found: {SQLITE_DB_PATH}")
        return

    print(f"Database found: {SQLITE_DB_PATH}")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("No tables found in the database.")
        conn.close()
        return

    print("\nTables in database:")

    for table in tables:
        table_name = table["name"]
        print(f"\n==============================")
        print(f"Table: {table_name}")
        print("==============================")

        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        print("Columns:")
        for col in columns:
            print(f"  - {col['name']} ({col['type']})")

        cursor.execute(f"SELECT COUNT(*) AS row_count FROM {table_name};")
        row_count = cursor.fetchone()["row_count"]
        print(f"Row count: {row_count}")

        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
        rows = cursor.fetchall()

        print("Sample rows:")
        for row in rows:
            print(dict(row))

    conn.close()


if __name__ == "__main__":
    inspect_database()