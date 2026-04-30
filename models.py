import sqlite3
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name, check_same_thread=False)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        if not self.connection:
            raise Exception("Database connection is not established.")
        
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Database query failed: {e} | Query: {query}")
            raise
    
def initialize_database(db):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS comics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        genres TEXT,
        description TEXT,
        cover_image TEXT,
        path TEXT NOT NULL,
        type TEXT,
        pages INTEGER,
        chapters INTEGER
    );
    """
    db.execute_query(create_table_query)

    existing_cols = [row[1] for row in db.execute_query("PRAGMA table_info(comics)")]

    for col, col_type in [("type", "TEXT"), ("pages", "INTEGER"), ("chapters", "INTEGER")]:
        if col not in existing_cols:
            try:
                db.execute_query(f"ALTER TABLE comics ADD COLUMN {col} {col_type}")
            except Exception as e:
                logger.debug(f"Column {col} alter table failed: {e}")
                pass