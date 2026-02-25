from app.core.database import execute_query
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_column_defaults():
    """
    Ensures that photo and document URL columns allow NULL values 
    to prevent errors during record creation.
    """
    commands = [
        "ALTER TABLE drivers MODIFY photo_url VARCHAR(255) DEFAULT NULL",
        "ALTER TABLE students MODIFY student_photo_url VARCHAR(255) DEFAULT NULL",
        "ALTER TABLE buses MODIFY rc_book_url VARCHAR(255) DEFAULT NULL",
        "ALTER TABLE buses MODIFY fc_certificate_url VARCHAR(255) DEFAULT NULL"
    ]
    
    for sql in commands:
        try:
            logger.info(f"Executing: {sql}")
            execute_query(sql)
            logger.info("Success.")
        except Exception as e:
            logger.error(f"Failed: {e}")

if __name__ == "__main__":
    fix_column_defaults()
