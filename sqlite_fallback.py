# SQLite Fallback Configuration
# Use this when MySQL server is completely unavailable

import sqlite3
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

@contextmanager
def get_sqlite_db():
    """SQLite fallback database connection"""
    connection = None
    try:
        connection = sqlite3.connect('school_app.db')
        connection.row_factory = sqlite3.Row  # Dict-like access
        yield connection
        connection.commit()
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(f"SQLite operation failed: {e}")
        raise e
    finally:
        if connection:
            connection.close()

def create_sqlite_tables():
    """Create basic tables in SQLite for emergency use"""
    with get_sqlite_db() as conn:
        cursor = conn.cursor()
        
        # Create admins table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                admin_id TEXT PRIMARY KEY,
                phone INTEGER UNIQUE,
                email TEXT,
                password_hash TEXT,
                name TEXT,
                dob DATE,
                status TEXT DEFAULT 'ACTIVE',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default admin
        cursor.execute('''
            INSERT OR IGNORE INTO admins (admin_id, phone, password_hash, name)
            VALUES ('admin-1', 9876543210, '$2b$12$hash', 'Emergency Admin')
        ''')
        
        print("SQLite emergency database created")

if __name__ == "__main__":
    create_sqlite_tables()