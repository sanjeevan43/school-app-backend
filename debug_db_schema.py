
import pymysql
from database import get_db

def inspect_table():
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DESCRIBE buses;")
                columns = cursor.fetchall()
                print("Columns in 'buses' table:")
                for col in columns:
                    print(col)
    except Exception as e:
        print(f"Error inspecting table: {e}")

if __name__ == "__main__":
    inspect_table()
