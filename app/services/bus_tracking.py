import logging
import math
import json
import asyncio
import uuid
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.core.database import execute_query
from app.notification_api.service import notification_service

logger = logging.getLogger(__name__)

class BusTrackingService:
    def __init__(self):
        pass
        
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
        if trip_type == "PICKUP":
            query = """
            SELECT s.student_id, s.name, ft.fcm_token, rs.stop_name, rs.location
            FROM students s
            JOIN route_stops rs ON s.pickup_stop_id = rs.stop_id
            LEFT JOIN fcm_tokens ft ON s.student_id = ft.student_id
            WHERE s.pickup_route_id = %s AND rs.pickup_stop_order = %s 
            AND s.transport_status = 'ACTIVE' AND s.student_status IN ('CURRENT', 'ACTIVE')
            AND s.is_transport_user = 1
            """
        else:  # DROP
            query = """
            SELECT s.student_id, s.name, ft.fcm_token, rs.stop_name, rs.location
            FROM students s
            JOIN route_stops rs ON s.drop_stop_id = rs.stop_id
            LEFT JOIN fcm_tokens ft ON s.student_id = ft.student_id
            WHERE s.drop_route_id = %s AND rs.drop_stop_order = %s 
            AND s.transport_status = 'ACTIVE' AND s.student_status IN ('CURRENT', 'ACTIVE')
            AND s.is_transport_user = 1
            """
        
        return execute_query(query, (route_id, stop_order), fetch_all=True) or []

    def get_students_for_location(self, route_id: str, location_name: str, trip_type: str) -> List[Dict]:
        """Get students for all stops that share the same location name on a route"""
        if not location_name:
            return []
            
        if trip_type == "PICKUP":
            query = """
            SELECT s.student_id, s.name, ft.fcm_token, rs.stop_name
            FROM students s
            JOIN route_stops rs ON s.pickup_stop_id = rs.stop_id
            LEFT JOIN fcm_tokens ft ON s.student_id = ft.student_id
            WHERE s.pickup_route_id = %s 
            AND (rs.location = %s OR ((rs.location IS NULL OR rs.location = '') AND rs.stop_name = %s))
            AND s.transport_status = 'ACTIVE' AND s.student_status IN ('CURRENT', 'ACTIVE')
            AND s.is_transport_user = 1
            """
            return execute_query(query, (route_id, location_name, location_name), fetch_all=True) or []
        else:  # DROP
            query = """
            SELECT s.student_id, s.name, ft.fcm_token, rs.stop_name
            FROM students s
            JOIN route_stops rs ON s.drop_stop_id = rs.stop_id
            LEFT JOIN fcm_tokens ft ON s.student_id = ft.student_id
            WHERE s.drop_route_id = %s 
            AND (rs.location = %s OR ((rs.location IS NULL OR rs.location = '') AND rs.stop_name = %s))
            AND s.transport_status = 'ACTIVE' AND s.student_status IN ('CURRENT', 'ACTIVE')
            AND s.is_transport_user = 1
            """
        return execute_query(query, (route_id, location_name, location_name), fetch_all=True) or []
    
    def get_parent_tokens_for_students(self, student_ids: List[str]) -> List[str]:
        """Get parent FCM tokens for given students"""
        if not student_ids:
            return []
            
        placeholders = ','.join(['%s'] * len(student_ids))
        query = f"""
        SELECT DISTINCT ft.fcm_token
        FROM students s
        JOIN fcm_tokens ft ON (s.student_id = ft.student_id OR s.parent_id = ft.parent_id OR s.s_parent_id = ft.parent_id)
        WHERE s.student_id IN ({placeholders}) AND ft.fcm_token IS NOT NULL
        """
        
        tokens = execute_query(query, tuple(student_ids), fetch_all=True)
        return [token['fcm_token'] for token in tokens if token['fcm_token']]
    
    def _get_system_admin_id(self) -> Optional[str]:
        """Cache and return a valid admin_id for logging notifications"""
        if not hasattr(self, '_cached_admin_id'):
            try:
                admin_res = execute_query("SELECT admin_id FROM admins WHERE status = 'ACTIVE' LIMIT 1", fetch_one=True)
                self._cached_admin_id = admin_res['admin_id'] if admin_res else None
            except Exception:
                self._cached_admin_id = None
        return self._cached_admin_id

    def _log_notification(self, title: str, message: str, route_id: str, location_name: str = None):
        """Helper to log notification to admin_parent_notifications table"""
        try:
            admin_id = self._get_system_admin_id()
            if admin_id:
                execute_query(
                    "INSERT INTO admin_parent_notifications (notification_id, title, message, recipient_type, route_id, location_name, sent_by_admin_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (str(uuid.uuid4()), title, message, "LOCATION", route_id, location_name, admin_id)
                )
        except Exception as e:
            logger.warning(f"Failed to log notification: {e}")

    async def update_bus_location(self, trip_id: str, latitude: float, longitude: float):
        """Automatic bus tracking - handle stop progression and trip completion"""
        try:
            # Update driver_live_locations table (current location store)
            update_live_query = """
            INSERT INTO driver_live_locations (driver_id, latitude, longitude, updated_at)
            SELECT driver_id, %s, %s, CURRENT_TIMESTAMP FROM trips WHERE trip_id = %s
            ON DUPLICATE KEY UPDATE 
                latitude = VALUES(latitude),
                longitude = VALUES(longitude),
                updated_at = CURRENT_TIMESTAMP
            """
            execute_query(update_live_query, (latitude, longitude, trip_id))

            # Get trip details
            trip_query = """
            SELECT t.*, r.name as route_name, b.registration_number
            FROM trips t
            JOIN routes r ON t.route_id = r.route_id
            JOIN buses b ON t.bus_id = b.bus_id
            WHERE t.trip_id = %s AND t.status IN ('ONGOING', 'NOT_STARTED')
            """
            trip = execute_query(trip_query, (trip_id,), fetch_one=True)
            
            if not trip:
                return {"success": False, "message": "Trip not found or not ongoing"}
            
            # Get route stops based on trip type
            order_field = "pickup_stop_order" if trip['trip_type'] == "PICKUP" else "drop_stop_order"
            # BUG FIX: Also filter out stops with NULL stop_order — without this, `s['stop_order'] > current_stop_order`
            # raises TypeError (NoneType > int) which crashes the entire function and silently kills all notifications.
            stops_query = f"""
            SELECT stop_id, stop_name, location, latitude, longitude, {order_field} as stop_order
            FROM route_stops 
            WHERE route_id = %s
              AND latitude IS NOT NULL AND longitude IS NOT NULL
              AND {order_field} IS NOT NULL
            ORDER BY {order_field}
            """
            
            stops = execute_query(stops_query, (trip['route_id'],), fetch_all=True)
            
            if not stops:
                return {"success": False, "message": "No stops with coordinates found"}

            current_stop_order = trip['current_stop_order']
            
            # --- Logic for First Stop 500m Alert (Stored in DB) ---
            if current_stop_order < 1 and not trip.get('is_first_stop_notified'):
                first_stop = next((s for s in stops if s['stop_order'] == 1), None)
                if first_stop:
                    dist_to_first = self.calculate_distance(
                        latitude, longitude,
                        float(first_stop['latitude']), float(first_stop['longitude'])
                    )
                    if dist_to_first <= 1.0: # 1000m (1km)
                        first_stop_loc = first_stop['location'] or first_stop['stop_name']
                        logger.info(f"🔔 Notifying first stop 1000m alert: {first_stop_loc}")
                        students = self.get_students_for_route_stop(trip['route_id'], 1, trip['trip_type'])
                        if students:
                            title = "🚌 Bus Nearby"
                            body = f"The bus is approaching {first_stop_loc}. Please be ready."
                            await self._broadcast_helper(students, title, body, {"trip_id": trip_id, "stop_name": first_stop_loc, "status": "UPCOMING"}, message_type="audio")
                            self._log_notification(title, body, trip['route_id'], first_stop_loc)
                        
                        execute_query("UPDATE trips SET is_first_stop_notified = 1 WHERE trip_id = %s", (trip_id,))
            
            # --- Smart Lookahead Stop Logic (Handles Skips) ---
            skipped_raw = trip.get('skipped_stops')
            if isinstance(skipped_raw, list):
                skipped_list = skipped_raw
            elif isinstance(skipped_raw, str):
                try:
                    skipped_list = json.loads(skipped_raw)
                except Exception:
                    skipped_list = []
            else:
                skipped_list = []
            
            # FIX: Use >= instead of > so that stops at current_stop_order are also considered
            # This fixes the case where skip_stop sets current_stop_order to the skipped stop's order
            # but the stop is in skipped_list, so lookahead correctly skips it and finds the next one
            lookahead_stops = [s for s in stops if s['stop_order'] > current_stop_order and s['stop_order'] not in skipped_list][:5]
            
            stops_passed = 0
            current_stop_info = None
            arrived_stop = None

            # Find if we have reached any of the upcoming stops
            for stop in lookahead_stops:
                distance = self.calculate_distance(
                    latitude, longitude, 
                    float(stop['latitude']), float(stop['longitude'])
                )
                
                # Check if we have REACHED the stop (within 500m)
                if distance <= 0.5: # reached stop (within 500m)
                    arrived_stop = stop
                    break

            if arrived_stop:
                target_order = arrived_stop['stop_order']
                
                # 0. Check if this LOCATION (not just stop) was already reached/notified
                original_logs = {}
                try:
                    logs_raw = trip.get('stop_logs')
                    if logs_raw:
                        original_logs = json.loads(logs_raw) if isinstance(logs_raw, str) else logs_raw
                except:
                    original_logs = {}
                
                current_loc_name = arrived_stop['location'] or arrived_stop['stop_name']
                
                # Find all stops sharing this location
                same_location_stops = [s for s in stops if (s['location'] or s['stop_name']) == current_loc_name]
                # FIX: Only treat a stop as "already notified" if the log entry is a real timestamp,
                # NOT if it was "SKIPPED". Skipped stops should not prevent arrival notifications.
                location_already_notified = any(
                    s['stop_id'] in original_logs and original_logs[s['stop_id']] != "SKIPPED"
                    for s in same_location_stops
                )
                
                logger.info(f"📍 Stop Reached: {arrived_stop['stop_name']} (Group: {current_loc_name}) | Notified: {location_already_notified}")
                
                # 1. Update Database (mark current and intermediate stops as reached)
                new_stop_logs = original_logs.copy()
                for s in stops:
                    if current_stop_order < s['stop_order'] <= target_order:
                        s_id = s['stop_id']
                        # Only set timestamp if not already set (preserve SKIPPED entries as-is, add timestamp for new ones)
                        if s_id not in new_stop_logs or new_stop_logs[s_id] == "SKIPPED":
                            # If it was skipped but we physically arrived, still mark intermediate ones
                            if s['stop_order'] == target_order or s['stop_order'] not in skipped_list:
                                new_stop_logs[s_id] = datetime.now().isoformat()
                                if s['stop_order'] < target_order:
                                    logger.warning(f"⚠️ Missed GPS update for intermediate stop: {s['stop_name']} (Order: {s['stop_order']}). Marking as reached implicitly.")

                update_query = """
                UPDATE trips SET 
                    current_stop_order = %s, 
                    stop_logs = %s,
                    updated_at = CURRENT_TIMESTAMP 
                WHERE trip_id = %s
                """
                execute_query(update_query, (target_order, json.dumps(new_stop_logs), trip_id))
                
                stops_passed = target_order - current_stop_order
                current_stop_order = target_order
                current_stop_info = {"stop_name": arrived_stop['stop_name'], "stop_order": target_order}

                # 2. Trigger Notifications ONLY if this is the FIRST stop in this location group
                if not location_already_notified:
                    # A. Arrival Notification (For all students at this location)
                    students_arrived = self.get_students_for_location(trip['route_id'], current_loc_name, trip['trip_type'])
                    if students_arrived:
                        title = "🚌 Bus Arrived"
                        message = f"The bus has arrived at {current_loc_name}."
                        await self._broadcast_helper(students_arrived, title, message, {"trip_id": trip_id, "location": current_loc_name, "status": "ARRIVED"}, message_type="audio")
                        self._log_notification(title, message, trip['route_id'], current_loc_name)
                        logger.info(f"📣 Sent Arrival Notification for {current_loc_name} to {len(students_arrived)} students")

                    # Find UNIQUE locations ahead to send approaching/nearby alerts once per area
                    remaining_stops = [s for s in stops if s['stop_order'] > target_order and s['stop_order'] not in skipped_list]
                    unique_locs_ahead = []
                    seen_locs = {current_loc_name}
                    for s in remaining_stops:
                        loc = s['location'] or s['stop_name']
                        if loc not in seen_locs:
                            unique_locs_ahead.append(loc)
                            seen_locs.add(loc)

                    # B. Upcoming Stops Notifications (Next 4 Unique Locations)
                    for i in range(min(len(unique_locs_ahead), 4)):
                        future_loc = unique_locs_ahead[i]
                        students_ahead = self.get_students_for_location(trip['route_id'], future_loc, trip['trip_type'])
                        if students_ahead:
                            if i == 0:
                                title = "🚌 Bus Approaching"
                                message = f"The bus has reached {current_loc_name} and will arrive at {future_loc} soon."
                                status_val = "APPROACHING"
                            else:
                                title = "🚌 Bus Update"
                                message = f"The bus has reached {current_loc_name}. Please be ready for your stop."
                                status_val = "UPCOMING"

                            await self._broadcast_helper(
                                students_ahead, 
                                title, 
                                message, 
                                {"trip_id": trip_id, "location": future_loc, "status": status_val}, 
                                message_type="audio"
                            )
                            self._log_notification(title, message, trip['route_id'], future_loc)
                            logger.info(f"📣 Sent '{status_val}' Notification for {future_loc} to {len(students_ahead)} students")


            # Per user request: do not automatically complete the trip or tell the UI it's completed.
            # The driver must manually complete it.
            trip_completed = False

            return {
                "success": True,
                "trip_id": trip_id,
                "current_stop_order": current_stop_order,
                "current_stop_info": current_stop_info,
                "stops_passed": stops_passed,
                "trip_completed": trip_completed,
                "message": f"Reached {current_stop_info['stop_name']}" if current_stop_info else "In transit"
            }
            
        except Exception as e:
            logger.error(f"Bus location processing error: {e}")
            return {"success": False, "error": str(e)}

    async def _broadcast_helper(self, students: List[Dict], title: str, body: str, data: Dict, message_type: str = "audio"):
        """Helper to broadcast notifications asynchronously"""
        if data is None:
            data = {}
        if "type" not in data:
            data["type"] = "proximity_alert"
            
        student_ids = [st['student_id'] for st in students]
        tokens = self.get_parent_tokens_for_students(student_ids)
        if tokens:
            await notification_service.broadcast_to_tokens(list(set(tokens)), title, body, data, message_type=message_type)
        else:
            logger.warning(f"⚠️ No FCM tokens found for parents of students: {student_ids}. Notification '{title}' not sent.")

    async def skip_specific_stop(self, trip_id: str, stop_order: int):
        """Mark a specific stop_order as skipped for the current trip"""
        try:
            query = "SELECT skipped_stops, stop_logs, trip_type, route_id, current_stop_order FROM trips WHERE trip_id = %s"
            result = execute_query(query, (trip_id,), fetch_one=True)
            if not result:
                return {"success": False, "message": "Trip not found"}

            current_order = result.get('current_stop_order', 0)
            if stop_order <= current_order:
                return {"success": False, "message": "Cannot skip a stop that the bus has already passed"}

            order_field = "pickup_stop_order" if result.get('trip_type') == "PICKUP" else "drop_stop_order"
            route_id = result.get('route_id')
            stops_query = f"""
            SELECT stop_id, stop_name, location, latitude, longitude, {order_field} as stop_order
            FROM route_stops 
            WHERE route_id = %s AND {order_field} IS NOT NULL
            ORDER BY {order_field}
            """
            stops = execute_query(stops_query, (route_id,), fetch_all=True) or []

            skipped_raw = result.get('skipped_stops')
            if isinstance(skipped_raw, list):
                skipped = skipped_raw
            elif isinstance(skipped_raw, str):
                try:
                    skipped = json.loads(skipped_raw)
                except Exception:
                    skipped = []
            else:
                skipped = []
                
            all_remaining_unskipped = [
                s for s in stops
                if s['stop_order'] > current_order and s['stop_order'] not in skipped
            ]
            
            if not all_remaining_unskipped:
                return {"success": False, "message": "No more stops to skip"}
                
            # Guard: Last stop
            if len(all_remaining_unskipped) == 1 and all_remaining_unskipped[0]['stop_order'] == stop_order:
                return {
                    "success": False,
                    "message": f"Cannot skip '{all_remaining_unskipped[0]['stop_name']}' — it is the last stop on this route."
                }
            
            # 2. Add new stop order if not already skipped
            if stop_order not in skipped:
                skipped.append(stop_order)
            
            # 3. Update stop_logs JSON trail (preserve existing entries)
            current_stop_logs = {}
            if result.get('stop_logs'):
                try:
                    current_stop_logs = json.loads(result['stop_logs']) if isinstance(result['stop_logs'], str) else result['stop_logs']
                except Exception:
                    current_stop_logs = {}
            
            # Find stop_id for this order to mark as SKIPPED
            target_stop_data = next((s for s in stops if s['stop_order'] == stop_order), None)
            if target_stop_data:
                current_stop_logs[target_stop_data['stop_id']] = "SKIPPED"

            # 4. Update DB
            execute_query(
                "UPDATE trips SET skipped_stops = %s, stop_logs = %s, updated_at = CURRENT_TIMESTAMP WHERE trip_id = %s",
                (json.dumps(skipped), json.dumps(current_stop_logs), trip_id)
            )

            logger.info(f"🚫 Stop {stop_order} manually excluded from trip {trip_id}")
            
            # Send Notification to students at that specific stop
            if target_stop_data:
                students_skipped = self.get_students_for_route_stop(route_id, stop_order, result.get('trip_type'))
                if students_skipped:
                    title = "🚌 Stop Skipped"
                    message = f"The bus will skip {target_stop_data['stop_name']} today."
                    await self._broadcast_helper(students_skipped, title, message, {"trip_id": trip_id, "status": "SKIPPED"})
            
            return {"success": True, "message": f"Stop {stop_order} skipped for this trip", "skipped_stops": skipped}
        except Exception as e:
            logger.error(f"Error skipping specific stop: {e}")
            return {"success": False, "error": str(e)}

    async def skip_stop(self, trip_id: str):
        """Manually skip the next target stop for a trip.
        
        Adds the skipped stop to skipped_stops list without advancing current_stop_order.
        The lookahead in update_bus_location naturally skips over it and finds the next real stop.
        """
        try:
            # 1. Get trip details
            trip_query = "SELECT * FROM trips WHERE trip_id = %s AND status = 'ONGOING'"
            trip = execute_query(trip_query, (trip_id,), fetch_one=True)
            if not trip:
                return {"success": False, "message": "Trip not found or not ongoing"}

            current_order = trip['current_stop_order']
            order_field = "pickup_stop_order" if trip['trip_type'] == "PICKUP" else "drop_stop_order"
            
            # BUG FIX: Filter NULL stop_orders — unordered stops would bubble to the top
            # of the sorted list and be incorrectly identified as "next stop".
            stops_query = f"""
            SELECT stop_id, stop_name, location, latitude, longitude, {order_field} as stop_order
            FROM route_stops 
            WHERE route_id = %s AND {order_field} IS NOT NULL
            ORDER BY {order_field}
            """
            stops = execute_query(stops_query, (trip['route_id'],), fetch_all=True) or []
            
            # Parse current skipped_stops list
            skipped_raw = trip.get('skipped_stops')
            if isinstance(skipped_raw, list):
                skipped_list = skipped_raw
            elif isinstance(skipped_raw, str):
                try:
                    skipped_list = json.loads(skipped_raw)
                except Exception:
                    skipped_list = []
            else:
                skipped_list = []

            # Collect all remaining unskipped stops (used both for guard and notifications)
            all_remaining_unskipped = [
                s for s in stops
                if s['stop_order'] > current_order and s['stop_order'] not in skipped_list
            ]

            if not all_remaining_unskipped:
                return {"success": False, "message": "No more stops to skip"}

            next_unskipped = all_remaining_unskipped[0]
            target_loc = next_unskipped['location'] or next_unskipped['stop_name']
            
            # Find all stops at this exact location
            stops_to_skip = [
                s for s in all_remaining_unskipped 
                if (s['location'] or s['stop_name']) == target_loc
            ]

            # BUG FIX: Guard against skipping the LAST stop
            if len(all_remaining_unskipped) <= len(stops_to_skip):
                return {
                    "success": False,
                    "message": f"Cannot skip '{target_loc}' — it includes the last stop on this route."
                }

            # 2. Add to skipped_stops list (DO NOT advance current_stop_order)
            for s in stops_to_skip:
                if s['stop_order'] not in skipped_list:
                    skipped_list.append(s['stop_order'])

            # 3. Update stop_logs to mark as SKIPPED
            current_stop_logs = {}
            if trip.get('stop_logs'):
                try:
                    current_stop_logs = json.loads(trip['stop_logs']) if isinstance(trip['stop_logs'], str) else trip['stop_logs']
                except Exception:
                    current_stop_logs = {}
            
            for s in stops_to_skip:
                current_stop_logs[s['stop_id']] = "SKIPPED"

            # 4. Update DB: keep current_stop_order the same, just update skipped_stops and stop_logs
            execute_query(
                "UPDATE trips SET skipped_stops = %s, stop_logs = %s, updated_at = CURRENT_TIMESTAMP WHERE trip_id = %s",
                (json.dumps(skipped_list), json.dumps(current_stop_logs), trip_id)
            )
            
            skipped_stop_name = target_loc
            target_skip_order = stops_to_skip[0]['stop_order']

            logger.info(f"⏭️ Manual Skip: Location {skipped_stop_name} (Order {target_skip_order})")

            # 4.5. Trigger notification to the SKIPPED stops
            for s in stops_to_skip:
                students_skipped = self.get_students_for_route_stop(trip['route_id'], s['stop_order'], trip['trip_type'])
                if students_skipped:
                    title = "🚌 Stop Skipped"
                    message = f"The bus will skip {s['stop_name']} today."
                    await self._broadcast_helper(students_skipped, title, message, {"trip_id": trip_id, "status": "SKIPPED"})

            # 5. Trigger notifications for the stops AFTER the skipped one
            # Recompute remaining after the skip so the skipped stop is excluded
            remaining_unskipped = [s for s in stops if s['stop_order'] > current_order and s['stop_order'] not in skipped_list]
            
            # A. Approaching Notification for the next unskipped stop
            if remaining_unskipped:
                next_actual = remaining_unskipped[0]
                students_N1 = self.get_students_for_route_stop(trip['route_id'], next_actual['stop_order'], trip['trip_type'])
                if students_N1:
                    title = "🚌 Bus Approaching"
                    message = f"The bus is skipping {skipped_stop_name} and will arrive at {next_actual['stop_name']} soon."
                    await self._broadcast_helper(students_N1, title, message, {"trip_id": trip_id, "stop_name": next_actual['stop_name'], "status": "APPROACHING"})

            # B. Upcoming Notification for subsequent unskipped stops (up to 4 more)
            for i in range(1, min(len(remaining_unskipped), 5)):
                future_stop = remaining_unskipped[i]
                students_future = self.get_students_for_route_stop(trip['route_id'], future_stop['stop_order'], trip['trip_type'])
                if students_future:
                    title = "🚌 Bus Nearby"
                    message = f"The bus is approaching {future_stop['stop_name']}. Please be ready."
                    await self._broadcast_helper(students_future, title, message, {"trip_id": trip_id, "status": "UPCOMING"})

            return {
                "success": True,
                "message": f"Stop '{skipped_stop_name}' skipped",
                "skipped_stop_order": target_skip_order,
                "skipped_stops": skipped_list
            }
        except Exception as e:
            logger.error(f"Manual skip error: {e}")
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
            AND s.student_status IN ('CURRENT', 'ACTIVE') AND s.is_transport_user = 1
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