import pymysql

conn = pymysql.connect(
    host='72.61.250.191',
    port=3306,
    user='myuser',
    password='Hope3Services@2026',
    database='selvagam_school_db',
    cursorclass=pymysql.cursors.DictCursor
)

tables = ["admins", "parents", "drivers", "buses", "routes", "students", "trips", "classes"]

try:
    with conn.cursor() as cur:
        for table in tables:
            for field in ["created_at", "updated_at"]:
                cur.execute(f"SELECT COUNT(*) as count FROM {table} WHERE {field} IS NULL")
                res = cur.fetchone()
                if res['count'] > 0:
                    print(f"❌ {table}.{field} has {res['count']} NULL rows!")
                    
        # Check parents phone numbers (required int)
        cur.execute("SELECT COUNT(*) as count FROM parents WHERE phone IS NULL")
        res = cur.fetchone()
        if res['count'] > 0:
            print(f"❌ parents.phone has {res['count']} NULL rows!")

finally:
    conn.close()
