import pymysql

def get_conn():
    return pymysql.connect(
        host='72.61.250.191',
        port=3306,
        user='myuser',
        password='Hope3Services@2026',
        database='selvagam_school_db',
        cursorclass=pymysql.cursors.DictCursor
    )

VALID_ENUMS = {
    "students": {
        "student_status": ["CURRENT", "ALUMNI", "DISCONTINUED", "LONG_ABSENT"],
        "transport_status": ["ACTIVE", "INACTIVE"]
    }
}

conn = get_conn()
try:
    with conn.cursor() as cur:
        for table, cols in VALID_ENUMS.items():
            for col, valid_list in cols.items():
                cur.execute(f"SELECT {col}, COUNT(*) as count FROM {table} GROUP BY {col}")
                results = cur.fetchall()
                for r in results:
                    val = r[col]
                    if val not in valid_list:
                        print(f"INVALID: {table}.{col} = {val} ({r['count']} rows)")
finally:
    conn.close()
