import requests
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import math
from app.core.database import execute_query
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class FCMService:
    def __init__(self, server_key: str = None):
        self.server_key = server_key or settings.FCM_SERVER_KEY
        self.fcm_url = "https://fcm.googleapis.com/fcm/send"
        
    def send_notification(self, tokens: List[str], title: str, body: str, data: Dict = None):
        """Send FCM notification to multiple tokens"""
        if not tokens:
            return {"success": False, "message": "No tokens provided"}
            
        headers = {
            "Authorization": f"key={self.server_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "registration_ids": tokens,
            "notification": {
                "title": title,
                "body": body,
                "sound": "default"
            },
            "data": data or {}
        }
        
        try:
            response = requests.post(self.fcm_url, headers=headers, json=payload)
            return {
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else response.text
            }
        except Exception as e:
            logger.error(f"FCM notification error: {e}")
            return {"success": False, "error": str(e)}

class BusTrackingService:
    def __init__(self):
        self.fcm_service = FCMService()
        
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers"""
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def get_students_for_route_stop(self, route_id: str, stop_order: int, trip_type: str) -> List[Dict]:
        """Get students for a specific route stop based on trip type"""
        if trip_type == "MORNING":
            query = """
            SELECT s.student_id, s.name, ft.fcm_token, rs.stop_name
            FROM students s
            JOIN route_stops rs ON s.pickup_stop_id = rs.stop_id
            LEFT JOIN fcm_tokens ft ON s.student_id = ft.student_id
            WHERE s.pickup_route_id = %s AND rs.pickup_stop_order = %s 
            AND s.transport_status = 'ACTIVE' AND s.student_status = 'CURRENT'
            AND s.is_transport_user = True
            """
        else:  # EVENING
            query = """
            SELECT s.student_id, s.name, ft.fcm_token, rs.stop_name
            FROM students s
            JOIN route_stops rs ON s.drop_stop_id = rs.stop_id
            LEFT JOIN fcm_tokens ft ON s.student_id = ft.student_id
            WHERE s.drop_route_id = %s AND rs.drop_stop_order = %s 
            AND s.transport_status = 'ACTIVE' AND s.student_status = 'CURRENT'
            AND s.is_transport_user = True
            """
        
        return execute_query(query, (route_id, stop_order), fetch_all=True) or []
    
    def get_parent_tokens_for_students(self, student_ids: List[str]) -> List[str]:
        """Get parent FCM tokens for given students"""
        if not student_ids:
            return []
            
        placeholders = ','.join(['%s'] * len(student_ids))
        query = f"""
        SELECT DISTINCT ft.fcm_token
        FROM students s
        JOIN fcm_tokens ft ON (s.parent_id = ft.parent_id OR s.s_parent_id = ft.parent_id)
        WHERE s.student_id IN ({placeholders}) AND ft.fcm_token IS NOT NULL
        """
        
        tokens = execute_query(query, tuple(student_ids), fetch_all=True)
        return [token['fcm_token'] for token in tokens if token['fcm_token']]
    
    def update_bus_location(self, trip_id: str, latitude: float, longitude: float):
        """Automatic bus tracking - handle stop progression and trip completion"""
        try:
            # Get trip details
            trip_query = """
            SELECT t.*, r.name as route_name, b.registration_number
            FROM trips t
            JOIN routes r ON t.route_id = r.route_id
            JOIN buses b ON t.bus_id = b.bus_id
            WHERE t.trip_id = %s AND t.status = 'ONGOING'
            """
            trip = execute_query(trip_query, (trip_id,), fetch_one=True)
            
            if not trip:
                return {"success": False, "message": "Trip not found or not ongoing"}
            
            # Get route stops based on trip type
            order_field = "pickup_stop_order" if trip['trip_type'] == "MORNING" else "drop_stop_order"
            stops_query = f"""
            SELECT stop_id, stop_name, latitude, longitude, {order_field} as stop_order
            FROM route_stops 
            WHERE route_id = %s AND latitude IS NOT NULL AND longitude IS NOT NULL
            ORDER BY {order_field}
            """
            
            stops = execute_query(stops_query, (trip['route_id'],), fetch_all=True)
            
            if not stops:
                return {"success": False, "message": "No stops with coordinates found"}
            
            current_stop_order = trip['current_stop_order']
            trip_completed = False
            stops_passed = 0
            current_stop_info = None
            
            # Check all upcoming stops for progression
            for stop in stops:
                if stop['stop_order'] > current_stop_order:
                    distance = self.calculate_distance(
                        latitude, longitude, 
                        float(stop['latitude']), float(stop['longitude'])
                    )
                    
                    # Auto-update current stop if very close (within 0.3km)
                    if distance <= 0.3:
                        execute_query(
                            "UPDATE trips SET current_stop_order = %s WHERE trip_id = %s",
                            (stop['stop_order'], trip_id)
                        )
                        current_stop_order = stop['stop_order']
                        stops_passed += 1
                        current_stop_info = {
                            "stop_name": stop['stop_name'],
                            "stop_order": stop['stop_order']
                        }
                        
                        # Check if this is the last stop - auto complete trip
                        if stop['stop_order'] == max(s['stop_order'] for s in stops):
                            execute_query(
                                "UPDATE trips SET status = 'COMPLETED', ended_at = CURRENT_TIMESTAMP WHERE trip_id = %s",
                                (trip_id,)
                            )
                            trip_completed = True
                            break
            
            return {
                "success": True,
                "trip_id": trip_id,
                "current_stop_order": current_stop_order,
                "current_stop_info": current_stop_info,
                "stops_passed": stops_passed,
                "trip_completed": trip_completed,
                "message": "Trip completed!" if trip_completed else (f"Reached {current_stop_info['stop_name']}" if current_stop_info else "In transit")
            }
            
        except Exception as e:
            logger.error(f"Bus location processing error: {e}")
            return {"success": False, "error": str(e)}
    
    def update_route_fcm_cache(self, route_id: str):
        """Update FCM token cache for route stops"""
        try:
            # Get all stops for route with student/parent FCM tokens
            query = """
            SELECT 
                rs.stop_id,
                rs.stop_name,
                rs.pickup_stop_order,
                rs.drop_stop_order,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'fcm_token', ft.fcm_token,
                        'parent_id', ft.parent_id,
                        'parent_name', p.name
                    )
                ) as fcm_data
            FROM route_stops rs
            LEFT JOIN students s ON (
                (rs.stop_id = s.pickup_stop_id AND s.pickup_route_id = rs.route_id) OR
                (rs.stop_id = s.drop_stop_id AND s.drop_route_id = rs.route_id)
            )
            LEFT JOIN fcm_tokens ft ON (s.student_id = ft.student_id OR s.parent_id = ft.parent_id OR s.s_parent_id = ft.parent_id)
            LEFT JOIN parents p ON ft.parent_id = p.parent_id
            WHERE rs.route_id = %s AND s.transport_status = 'ACTIVE' 
            AND s.student_status = 'CURRENT' AND s.is_transport_user = True
            AND ft.fcm_token IS NOT NULL
            GROUP BY rs.stop_id, rs.stop_name, rs.pickup_stop_order, rs.drop_stop_order
            """
            
            stops_data = execute_query(query, (route_id,), fetch_all=True)
            
            # Create FCM cache map
            fcm_map = {}
            for stop in stops_data:
                fcm_map[stop['stop_id']] = {
                    "stop_name": stop['stop_name'],
                    "pickup_order": stop['pickup_stop_order'],
                    "drop_order": stop['drop_stop_order'],
                    "fcm_tokens": json.loads(stop['fcm_data']) if stop['fcm_data'] else []
                }
            
            # Update cache table
            cache_query = """
            INSERT INTO route_stop_fcm_cache (route_id, stop_fcm_map) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE 
            stop_fcm_map = VALUES(stop_fcm_map),
            updated_at = CURRENT_TIMESTAMP
            """
            
            execute_query(cache_query, (route_id, json.dumps(fcm_map)))
            
            return {"success": True, "route_id": route_id, "stops_cached": len(fcm_map)}
            
        except Exception as e:
            logger.error(f"FCM cache update error: {e}")
            return {"success": False, "error": str(e)}

# Global instances
bus_tracking_service = BusTrackingService()
fcm_service = FCMService()