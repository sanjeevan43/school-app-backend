import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from config import get_settings

settings = get_settings()

def get_db_connection():
    """Create a database connection"""
    return pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        cursorclass=DictCursor,
        autocommit=False
    )

@contextmanager
def get_db():
    """Context manager for database connections"""
    connection = get_db_connection()
    try:
        yield connection
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

def execute_query(query: str, params: tuple = None, fetch_one: bool = False, fetch_all: bool = False):
    """Execute a query and return results"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                return cursor.rowcount
