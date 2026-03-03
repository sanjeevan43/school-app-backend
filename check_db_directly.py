from app.core.database import execute_query
import json
trip_id = "f67002e4-b9c0-42ad-ad83-1adacfa70933"
result = execute_query("SELECT current_stop_order, skipped_stops FROM trips WHERE trip_id = %s", (trip_id,), fetch_one=True)
print(f"Result: {result}")
