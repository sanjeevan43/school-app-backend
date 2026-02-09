
from database import execute_query
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_bus_enum():
    try:
        # Check current schema first to know what we are dealing with
        print("Reverting to ENUM and adding MAINTENANCE...")
        
        # We need to explicitly list ALL allowed values
        query = "ALTER TABLE buses MODIFY COLUMN status ENUM('ACTIVE', 'INACTIVE', 'MAINTENANCE') DEFAULT 'ACTIVE';"
        execute_query(query)
        
        print("Successfully updated 'buses' table to ENUM with MAINTENANCE.")
        
    except Exception as e:
        print(f"Error updating schema: {e}")

if __name__ == "__main__":
    fix_bus_enum()
