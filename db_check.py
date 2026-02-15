from app.core.database import execute_query

checks = [
    ("admins", "status"),
    ("parents", "parents_active_status"),
    ("parents", "parent_role"),
    ("drivers", "status"),
    ("buses", "status"),
    ("routes", "routes_active_status"),
    ("classes", "status"),
    ("students", "student_status"),
    ("students", "transport_status"),
    ("trips", "status"),
    ("trips", "trip_type"),
]

print("Checking for NULLs or Enums in DB...")
for table, column in checks:
    try:
        query = f"SELECT {column}, COUNT(*) as count FROM {table} GROUP BY {column}"
        results = execute_query(query, fetch_all=True)
        print(f"\n--- {table}.{column} ---")
        if not results:
            print("  (Empty Table)")
        for r in results:
            print(f"  Value: {r[column]} | Count: {r['count']}")
    except Exception as e:
        print(f"  Error checking {table}.{column}: {e}")
