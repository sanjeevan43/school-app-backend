import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from config import get_settings
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

def get_db_connection():
    """Create a database connection"""
    try:
        return pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            cursorclass=DictCursor,
            autocommit=False,
            charset='utf8mb4'
        )
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

@contextmanager
def get_db():
    """Context manager for database connections"""
    connection = None
    try:
        connection = get_db_connection()
        yield connection
        connection.commit()
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(f"Database operation failed: {e}")
        raise e
    finally:
        if connection:
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
