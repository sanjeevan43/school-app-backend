
from database import execute_query
import logging

logging.basicConfig(level=logging.INFO)

def fix_schema():
    print("Fixing database schema...")
    
    # 1. Update BUS schema to include SCRAP and SPARE
    try:
        print("Modifying BUS status enum...")
        query = "ALTER TABLE buses MODIFY COLUMN status ENUM('ACTIVE', 'INACTIVE', 'MAINTENANCE', 'SCRAP', 'SPARE') DEFAULT 'ACTIVE'"
        execute_query(query)
        print("✅ BUS status enum updated: ACTIVE, INACTIVE, MAINTENANCE, SCRAP, SPARE")
    except Exception as e:
        print(f"⚠️ Error updating BUS enum: {e}")

    # 2. Update DRIVER schema to include SUSPENDED and RESIGNED
    try:
        print("Modifying DRIVER status enum...")
        query = "ALTER TABLE drivers MODIFY COLUMN status ENUM('ACTIVE', 'INACTIVE', 'SUSPENDED', 'RESIGNED') DEFAULT 'ACTIVE'"
        execute_query(query)
        print("✅ DRIVER status enum updated: ACTIVE, INACTIVE, SUSPENDED, RESIGNED")
    except Exception as e:
        print(f"⚠️ Error updating DRIVER enum: {e}")

if __name__ == "__main__":
    fix_schema()
