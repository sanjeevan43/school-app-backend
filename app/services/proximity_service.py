import logging
import asyncio
import os
import httpx
from typing import Dict, Any, List, Set, Optional
from geopy.distance import distance as geodesic
from app.notification_api.service import notification_service
from app.core.database import execute_query

logger = logging.getLogger(__name__)

# Constants
APPROACHING_RADIUS = int(os.getenv("GEOFENCE_RADIUS", 500))  # meters
ARRIVED_RADIUS = 20       # meters

class ProximityTrackingService:
    def __init__(self):
        # In-memory storage for active tracking state
        self.active_trips: Dict[str, Dict[str, Any]] = {}
        self.notified_stops: Dict[str, Set[str]] = {}
        self.main_backend_url = os.getenv("MAIN_BACKEND_URL", "http://localhost:8080/api/v1")

    async def fetch_tokens_by_route(self, route_id: str) -> List[str]:
        """Fetch all parent tokens for a route (simplified fallback)"""
        try:
            query = """
            SELECT DISTINCT ft.fcm_token 
            FROM fcm_tokens ft
            JOIN students s ON (ft.student_id = s.student_id OR ft.parent_id = s.parent_id OR ft.parent_id = s.s_parent_id)
            WHERE (s.pickup_route_id = %s OR s.drop_route_id = %s)
            AND ft.fcm_token IS NOT NULL
            """
            results = execute_query(query, (route_id, route_id), fetch_all=True)
            return [r['fcm_token'] for r in results if r['fcm_token']]
        except Exception as e:
            logger.error(f"Error fetching route tokens: {e}")
            return []

    async def fetch_route_stops(self, route_id: str) -> List[Dict]:
        """Fetch stops for a route with coordinates"""
        try:
            query = """
            SELECT stop_id, stop_name, latitude, longitude, pickup_stop_order
            FROM route_stops
            WHERE route_id = %s
            ORDER BY pickup_stop_order
            """
            return execute_query(query, (route_id,), fetch_all=True) or []
        except Exception as e:
            logger.error(f"Error fetching route stops: {e}")
            return []

    async def process_location_update(self, trip_id: str, lat: float, lng: float):
        """Core proximity logic moved from notification_app"""
        logger.info(f"📍 Proximity Check: {trip_id} -> {lat}, {lng}")
        
        # Initialize trip state if missing
        if trip_id not in self.active_trips:
            try:
                # Get trip details from DB
                trip_query = "SELECT route_id FROM trips WHERE trip_id = %s"
                trip = execute_query(trip_query, (trip_id,), fetch_one=True)
                if not trip:
                    return {"success": False, "message": "Trip not found"}
                
                route_id = trip['route_id']
                stops = await self.fetch_route_stops(route_id)
                
                self.active_trips[trip_id] = {
                    "trip_id": trip_id,
                    "route_id": route_id,
                    "stops": stops,
                    "tokens_by_stop": {}  # Lazy loaded
                }
                self.notified_stops[trip_id] = set()
                logger.info(f"✅ Initialized tracking for trip {trip_id}")
            except Exception as e:
                logger.error(f"Error initializing proximity trip {trip_id}: {e}")
                return {"success": False, "error": str(e)}

        trip_data = self.active_trips[trip_id]
        current_notified = self.notified_stops[trip_id]
        current_loc = (lat, lng)
        stops = trip_data.get("stops", [])
        route_id = trip_data.get("route_id")
        
        results = []

        for stop in stops:
            stop_id = stop.get("stop_id")
            stop_name = stop.get("stop_name")
            try:
                stop_lat = float(stop.get("latitude"))
                stop_lng = float(stop.get("longitude"))
            except (TypeError, ValueError):
                continue
                
            stop_loc = (stop_lat, stop_lng)
            dist = geodesic(current_loc, stop_loc).meters
            
            # --- Arrived Logic ---
            if dist <= ARRIVED_RADIUS:
                event_key = f"{stop_id}_arrived"
                if event_key not in current_notified:
                    logger.info(f"✨ ARRIVED at {stop_name} (dist: {dist:.1f}m)")
                    current_notified.add(event_key)
                    
                    # Fetch tokens for THIS stop specifically
                    tokens = await self.get_stop_tokens(route_id, stop_id)
                    if tokens:
                        await notification_service.broadcast_to_tokens(
                            tokens, 
                            "🚌 Bus Arrived", 
                            f"The bus has arrived at {stop_name}.",
                            {"trip_id": trip_id, "stop_id": stop_id, "status": "ARRIVED", "stop_name": stop_name}
                        )
                    results.append(f"Notified Arrived: {stop_name}")
            
            # --- Approaching Logic ---
            elif dist <= APPROACHING_RADIUS:
                event_key = f"{stop_id}_approaching"
                if event_key not in current_notified:
                    logger.info(f"🔔 APPROACHING {stop_name} (dist: {dist:.1f}m)")
                    current_notified.add(event_key)
                    
                    tokens = await self.get_stop_tokens(route_id, stop_id)
                    if tokens:
                        await notification_service.broadcast_to_tokens(
                            tokens, 
                            "🚌 Bus Approaching", 
                            f"The bus is approaching {stop_name}. Please be ready.",
                            {"trip_id": trip_id, "stop_id": stop_id, "status": "APPROACHING", "stop_name": stop_name}
                        )
                    results.append(f"Notified Approaching: {stop_name}")

        return {
            "success": True, 
            "trip_id": trip_id, 
            "notifications_sent": results
        }

    async def get_stop_tokens(self, route_id: str, stop_id: str) -> List[str]:
        """Fetch tokens for students at a specific stop"""
        try:
            query = """
            SELECT DISTINCT ft.fcm_token
            FROM students s
            JOIN fcm_tokens ft ON (s.student_id = ft.student_id OR s.parent_id = ft.parent_id OR s.s_parent_id = ft.parent_id)
            WHERE (s.pickup_stop_id = %s OR s.drop_stop_id = %s)
            AND (s.pickup_route_id = %s OR s.drop_route_id = %s)
            AND ft.fcm_token IS NOT NULL
            AND s.transport_status = 'ACTIVE'
            """
            results = execute_query(query, (stop_id, stop_id, route_id, route_id), fetch_all=True)
            return [r['fcm_token'] for r in results]
        except Exception as e:
            logger.error(f"Error fetching stop tokens: {e}")
            return []

    async def start_trip(self, trip_id: str, route_id: str):
        """Manual Start Trip Logic"""
        tokens = await self.fetch_tokens_by_route(route_id)
        if tokens:
            await notification_service.broadcast_to_tokens(
                tokens, "🚌 Bus Started", "Your bus has started the trip", 
                {"trip_id": trip_id, "route_id": route_id, "status": "STARTED"}
            )
        return {"success": True, "recipients": len(tokens)}

    async def complete_trip(self, trip_id: str, route_id: str):
        """Manual Complete Trip Logic"""
        tokens = await self.fetch_tokens_by_route(route_id)
        if tokens:
            await notification_service.broadcast_to_tokens(
                tokens, "✅ Trip Completed", "Your bus has completed the trip", 
                {"trip_id": trip_id, "route_id": route_id, "status": "COMPLETED"}
            )
        
        # Cleanup state
        if trip_id in self.active_trips:
            del self.active_trips[trip_id]
        if trip_id in self.notified_stops:
            del self.notified_stops[trip_id]
            
        return {"success": True, "recipients": len(tokens)}

# Global instance
proximity_service = ProximityTrackingService()
