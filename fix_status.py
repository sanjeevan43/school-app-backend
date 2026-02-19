from app.core.database import execute_query
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_student_status():
    try:
        # Update any student with 'GRADUATED' status to 'ALUMNI'
        # Since GRADUATED was removed from code, we treat it as a string here
        logger.info("Checking for students with invalid 'GRADUATED' status...")
        
        # We can't select with WHERE status='GRADUATED' via ORM if mapped, 
        # but raw SQL is fine.
        
        query_check = "SELECT COUNT(*) as count FROM students WHERE student_status = 'GRADUATED'"
        res = execute_query(query_check, fetch_one=True)
        count = res['count'] if res else 0
        
        if count > 0:
            logger.info(f"Found {count} students with 'GRADUATED' status. Updating to 'ALUMNI'...")
            update_query = "UPDATE students SET student_status = 'ALUMNI' WHERE student_status = 'GRADUATED'"
            execute_query(update_query)
            logger.info("Successfully updated student statuses.")
        else:
            logger.info("No students found with 'GRADUATED' status.")
            
    except Exception as e:
        logger.error(f"Error fixing student status: {e}")

if __name__ == "__main__":
    fix_student_status()
