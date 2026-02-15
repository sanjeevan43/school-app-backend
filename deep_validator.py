from app.core.database import execute_query

# Target Enums from models.py
VALID_ENUMS = {
    "students": {
        "student_status": ["CURRENT", "ALUMNI", "DISCONTINUED", "LONG_ABSENT"],
        "transport_status": ["ACTIVE", "INACTIVE"]
    },
    "parents": {
        "parents_active_status": ["ACTIVE", "INACTIVE"],
        "parent_role": ["FATHER", "MOTHER", "GUARDIAN"]
    },
    "drivers": {
        "status": ["ACTIVE", "INACTIVE", "SUSPENDED", "RESIGNED"]
    },
    "buses": {
        "status": ["ACTIVE", "INACTIVE", "MAINTENANCE", "SCRAP", "SPARE"]
    },
    "routes": {
        "routes_active_status": ["ACTIVE", "INACTIVE"]
    }
}

print("Deep Validation of Table Enums...")
errors_found = False

for table, cols in VALID_ENUMS.items():
    for col, valid_list in cols.items():
        try:
            query = f"SELECT {col}, COUNT(*) as count FROM {table} GROUP BY {col}"
            results = execute_query(query, fetch_all=True)
            if not results:
                continue
            
            for r in results:
                val = r[col]
                if val not in valid_list:
                    print(f"❌ INVALID DATA: table '{table}', column '{col}' has value '{val}' ({r['count']} rows)")
                    print(f"   Expected one of: {valid_list}")
                    errors_found = True
        except Exception as e:
            print(f"⚠️ Error checking {table}.{col}: {e}")

if not errors_found:
    print("✅ No Enum mismatches found in major tables.")
else:
    print("🚩 Please fix the invalid data listed above.")
