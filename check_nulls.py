import pymysql

conn = pymysql.connect(
    host='72.61.250.191',
    port=3306,
    user='myuser',
    password='Hope3Services@2026',
    database='selvagam_school_db',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with conn.cursor() as cur:
        # Check students for required fields that might be NULL
        required_fields = ["pickup_route_id", "drop_route_id", "pickup_stop_id", "drop_stop_id", "study_year"]
        for field in required_fields:
            cur.execute(f"SELECT COUNT(*) as count FROM students WHERE {field} IS NULL")
            res = cur.fetchone()
            if res['count'] > 0:
                print(f"❌ student.{field} has {res['count']} NULL rows!")
                
        # Also check for empty strings or invalid values in these IDs
        for field in ["pickup_route_id", "drop_route_id", "pickup_stop_id", "drop_stop_id"]:
            cur.execute(f"SELECT COUNT(*) as count FROM students WHERE {field} = ''")
            res = cur.fetchone()
            if res['count'] > 0:
                print(f"❌ student.{field} has {res['count']} EMPTY string rows!")

finally:
    conn.close()
