import logging
from datetime import datetime, timedelta
from app.core.database import execute_query

logger = logging.getLogger(__name__)

class CleanupService:
    """Service to handle periodic data pruning"""
    
    def prune_old_data(self, days: int = 30):
        """
        Delete logs older than the specified number of days.
        Currently handles:
        - Trips logs (completed or canceled)
        - Notification logs
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            cutoff_str = cutoff_date.strftime('%Y-%m-%d %H:%M:%S')
            
            logger.info(f"Starting data pruning for records older than {cutoff_str} ({days} days)")
            
            # 1. Prune Notification Logs
            # admin_parent_notifications table
            notif_query = "DELETE FROM admin_parent_notifications WHERE created_at < %s"
            notif_result = execute_query(notif_query, (cutoff_str,))
            logger.info(f"Pruned {notif_result} old notification logs")
            
            # 2. Prune Trip Logs
            # trips table - We only prune COMPLETED or CANCELED trips
            # Using created_at for pruning logic
            trip_query = "DELETE FROM trips WHERE created_at < %s AND status IN ('COMPLETED', 'CANCELED')"
            trip_result = execute_query(trip_query, (cutoff_str,))
            logger.info(f"Pruned {trip_result} old trip logs")
            
            return {
                "notifications_pruned": notif_result,
                "trips_pruned": trip_result,
                "cutoff_date": cutoff_str
            }
            
        except Exception as e:
            logger.error(f"Data pruning error: {e}")
            return False

# Global instance
cleanup_service = CleanupService()
