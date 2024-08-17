import os


from pathlib import Path
from sqlite3 import connect
from sqlite3 import Cursor, Connection, IntegrityError

conn: Connection | None = None
cursor: Cursor | None = None


def get_db(name: str | None = None, reset: bool = False):
    """
    Connect to SQLite3 database file(*.db)
    """
    global conn, cursor

    os.environ["CRYPTID_SQLITE_DB"] = ":memory"
    if conn:
        if not reset:
            return
        conn = None
    if not name:
        name = os.getenv("CRYPTID_SQLITE_DB")
        top_dir = Path(__file__).resolve().parents[1]

        db_dir = top_dir / "db"
        db_dir.mkdir(exist_ok=True)
        dbname = "cryptid.db"
        dbpath = str(db_dir / dbname)
        name = os.getenv("CRYPTID_SQLITE_DB", dbpath)

        if name == ":memory":
            name = ":memory:"

    conn = connect(name, check_same_thread=False)
    conn.isolation_level = None
    cursor = conn.cursor()


get_db()
