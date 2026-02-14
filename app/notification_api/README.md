# 🔥 FCM Notification API Setup (Python Version)

## ⚠️ CRITICAL: Firebase Credentials Required

**BEFORE STARTING:** You need Firebase service account credentials.

### Setup Instructions:
1. Go to Firebase Console → Project Settings → Service Accounts
2. Click "Generate new private key"
3. Download the JSON file and rename it to `firebase-credentials.json`
4. Place it in the project root or `src/` directory.

## 🚀 Quick Start (Python)

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python src/server.py

# Expected output:
# 🚀 FCM API running on http://0.0.0.0:8082
```

## 🧪 Test API

```bash
curl -X POST http://localhost:8082/api/send-notification \
  -H "Content-Type: application/json" \
  -H "x-admin-key: selvagam-admin-key-2024" \
  -d '{"title": "Test", "body": "API Working", "topic": "drivers"}'
```

## 📱 Mobile App Setup

```dart
// Subscribe to topics
FirebaseMessaging.instance.subscribeToTopic("drivers");
FirebaseMessaging.instance.subscribeToTopic("parents");
FirebaseMessaging.instance.subscribeToTopic("all_users");

// Handle notifications
FirebaseMessaging.onMessage.listen((message) {
  print('Title: ${message.notification?.title}');
  print('Body: ${message.notification?.body}');
});
```

## ✅ Deployment Checklist

- [ ] Place `firebase-credentials.json` in the root or `src/` directory
- [ ] Run `pip install -r requirements.txt`
- [ ] Ensure port `8082` is open
- [ ] Test API endpoint with `x-admin-key` header