# 📣 Selvagam School Notification Documentation

This document explains how to use the notification system to send messages to Parents, Drivers, and Students via Firebase Cloud Messaging (FCM).

---

## 🔐 Authentication
All notification endpoints require the following header for security:

| Header Key | Value |
| :--- | :--- |
| `x-admin-key` | `selvagam-admin-key-2024` |

---

## 📡 Status Check
Before sending notifications, check if the service is online and the Firebase credentials are correctly loaded.

**Endpoint:** `GET /api/notifications/status`

**Success Response:**
```json
{
  "status": "online",
  "initialized": true,
  "creds_found": true
}
```

---

## 🚀 Sending Notifications

### 1. Broadcast to All Parents
Sends a notification to every registered parent device in the system.
**Endpoint:** `POST /api/notifications/broadcast/parents`
```json
{
  "title": "School Holiday",
  "body": "Tomorrow is a holiday due to local festival."
}
```

### 2. Broadcast to All Drivers
Sends a notification to every active driver's app.
**Endpoint:** `POST /api/notifications/broadcast/drivers`
```json
{
  "title": "New Route Update",
  "body": "Please check your updated route map for tomorrow morning."
}
```

### 3. Send to a Specific Route
Notifies all parents and students assigned to a specific bus route ID.
**Endpoint:** `POST /api/notifications/route/{route_id}`
```json
{
  "title": "Delay Alert: Route 5",
  "body": "The bus is running 15 minutes late due to traffic."
}
```

### 4. Send to a Specific Student/Parent
**Endpoint:** `POST /api/notifications/student/{student_id}` (Notifies the child's guardians)
**Endpoint:** `POST /api/notifications/parent/{parent_id}` (Notifies specific parent)

---

## 📱 Mobile App Integration (Technical Details)

When a notification is sent from the backend, the mobile app receives both a **Notification** (visible alert) and a **Data Payload** (hidden logic).

### Data Payload Format:
Your app should listen for these keys in the notification data:

| Key | Description |
| :--- | :--- |
| `type` | Always `admin_notification` |
| `messageType` | Usually `text` |
| `recipientType` | One of: `parent`, `driver`, `student`, `route` |
| `timestamp` | Unix timestamp in milliseconds |
| `source` | Always `admin_panel` |
| `message` | The actual body text |

### Firebase Topic Subscription:
While the backend now uses direct token delivery for higher reliability, the app can still subscribe to these topics for mass messaging:
*   `all_users`
*   `parents`
*   `drivers`

---

## 🛠 Troubleshooting

1.  **"Firebase not initialized"**: 
    *   Ensure `firebase-credentials.json` is in the project root.
    *   Check if the JSON file has the correct `project_id`.
2.  **"No FCM tokens found"**:
    *   The user must log in to the mobile app at least once to register their phone's token in the database.
3.  **Notification not appearing**:
    *   Check if the phone has "Notifications" enabled for the app.
    *   The backend sends with `priority: high`, which should bypass battery optimization on Android.
