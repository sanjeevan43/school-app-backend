from app.core.database import execute_query
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_columns():
    alterations = [
        ("drivers", "photo_url", "VARCHAR(255) DEFAULT NULL AFTER licence_expiry"),
        ("students", "student_photo_url", "VARCHAR(255) DEFAULT NULL AFTER study_year"),
        ("buses", "rc_book_url", "VARCHAR(255) DEFAULT NULL AFTER fc_expiry_date"),
        ("buses", "fc_certificate_url", "VARCHAR(255) DEFAULT NULL AFTER rc_book_url")
    ]
    
    for table, column, definition in alterations:
        try:
            # Check if column exists
            check_query = f"SHOW COLUMNS FROM {table} LIKE '{column}'"
            exists = execute_query(check_query, fetch_one=True)
            
            if not exists:
                logger.info(f"Adding column {column} to table {table}...")
                alter_query = f"ALTER TABLE {table} ADD COLUMN {column} {definition}"
                execute_query(alter_query)
                logger.info(f"Successfully added {column} to {table}.")
            else:
                logger.info(f"Column {column} already exists in {table}.")
        except Exception as e:
            logger.error(f"Error updating table {table}: {e}")

if __name__ == "__main__":
    add_columns()
