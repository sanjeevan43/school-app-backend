from app.core.database import execute_query

# Fix student_status
print("Fixing invalid student_status values...")
q1 = "UPDATE students SET student_status = 'CURRENT' WHERE student_status = 'ACTIVE' OR student_status IS NULL"
res1 = execute_query(q1)
print(f"Updated {res1} rows in students.")

# Check for any other potentially invalid enums
# Parents active status
print("Standardizing parent status...")
q2 = "UPDATE parents SET parents_active_status = 'ACTIVE' WHERE parents_active_status = 'true' OR parents_active_status IS NULL"
res2 = execute_query(q2)
print(f"Updated {res2} rows in parents.")

q3 = "UPDATE parents SET parents_active_status = 'INACTIVE' WHERE parents_active_status = 'false'"
res3 = execute_query(q3)
print(f"Updated {res3} rows in parents (inactive).")

print("Done.")
