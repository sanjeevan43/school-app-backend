
from database import execute_query

def check_trips_table():
    try:
        print("Checking trips table schema...")
        result = execute_query("SHOW CREATE TABLE trips", fetch_one=True)
        print(result['Create Table'])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_trips_table()
