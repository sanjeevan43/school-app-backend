from app.core.database import execute_query
import json

def debug_route_data(route_id):
    print(f"--- Debugging Route: {route_id} ---")
    
    # 1. Total stops on route
    stops = execute_query("SELECT * FROM route_stops WHERE route_id = %s", (route_id,), fetch_all=True)
    print(f"Total stops on route: {len(stops)}")
    
    # 2. Students on route
    students = execute_query("SELECT student_id, name, pickup_stop_id, drop_stop_id, transport_status, student_status FROM students WHERE pickup_route_id = %s OR drop_route_id = %s", (route_id, route_id), fetch_all=True)
    print(f"Total students on route: {len(students)}")
    for s in students:
        print(f"  Student: {s['name']} (ID: {s['student_id']}), Pickup Stop: {s['pickup_stop_id']}, Status: {s['transport_status']}")
    
    # 3. FCM Tokens
    tokens = execute_query("SELECT * FROM fcm_tokens", fetch_all=True)
    print(f"Total FCM tokens in DB: {len(tokens)}")
    
    # 4. Check if any student on route has a token
    for s in students:
        tk_query = "SELECT * FROM fcm_tokens WHERE student_id = %s OR parent_id = %s"
        # We need to find the parent_id for the student
        p_query = "SELECT parent_id, s_parent_id FROM students WHERE student_id = %s"
        parents = execute_query(p_query, (s['student_id'],), fetch_one=True)
        
        s_tokens = execute_query("SELECT fcm_token FROM fcm_tokens WHERE student_id = %s OR parent_id = %s OR parent_id = %s", (s['student_id'], parents['parent_id'], parents['s_parent_id']), fetch_all=True)
        if s_tokens:
            print(f"  Token found for student {s['name']}: {len(s_tokens)} tokens")
        else:
            print(f"  NO token for student {s['name']}")

try:
    # Let's try to find a route ID first
    routes = execute_query("SELECT route_id, name FROM routes LIMIT 5", fetch_all=True)
    if routes:
        for r in routes:
            debug_route_data(r['route_id'])
    else:
        print("No routes found!")
except Exception as e:
    print(f"Error: {e}")
