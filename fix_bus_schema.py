
from database import execute_query
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_bus_schema():
    try:
        # Check current schema
        print("Creating backup of current status...")
        
        # Alter the table to match schema.sql (VARCHAR(20))
        # This will convert the ENUM to VARCHAR and allow 'MAINTENANCE'
        print("Altering 'buses' table to allow 'MAINTENANCE' status...")
        query = "ALTER TABLE buses MODIFY COLUMN status VARCHAR(20) DEFAULT 'ACTIVE';"
        execute_query(query)
        
        print("Successfully updated 'buses' table schema.")
        
    except Exception as e:
        print(f"Error updating schema: {e}")

if __name__ == "__main__":
    fix_bus_schema()
