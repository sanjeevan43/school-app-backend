from database import get_db

with get_db() as conn:
    with conn.cursor() as cursor:
        cursor.execute("DESCRIBE admins")
        print("Admins table structure:")
        for row in cursor.fetchall():
            print(row)
        
        cursor.execute("DESCRIBE parents")
        print("\nParents table structure:")
        for row in cursor.fetchall():
            print(row)
        
        cursor.execute("DESCRIBE drivers")
        print("\nDrivers table structure:")
        for row in cursor.fetchall():
            print(row)