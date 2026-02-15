from app.core.database import execute_query

res = execute_query('SHOW VARIABLES LIKE "max_connections"', fetch_one=True)
print(f"Max Connections: {res}")

res2 = execute_query('SHOW STATUS LIKE "Threads_connected"', fetch_one=True)
print(f"Threads Connected: {res2}")
