
from database import execute_query
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_bus_enum_all():
    try:
        print("Adding SCRAP and SPARE to bus status ENUM...")
        
        # Include ALL desired values
        query = "ALTER TABLE buses MODIFY COLUMN status ENUM('ACTIVE', 'INACTIVE', 'MAINTENANCE', 'SCRAP', 'SPARE') DEFAULT 'ACTIVE';"
        execute_query(query)
        
        print("Success! Bus status options are now: ACTIVE, INACTIVE, MAINTENANCE, SCRAP, SPARE")
        
    except Exception as e:
        print(f"Error updating schema: {e}")

if __name__ == "__main__":
    update_bus_enum_all()
