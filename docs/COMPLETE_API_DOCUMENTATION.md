# 🚌 School Transport Management API - Complete Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Dashboard APIs](#dashboard-apis)
3. [Authentication APIs](#authentication-apis)
4. [Admin APIs](#admin-apis)
5. [Parent APIs](#parent-apis)
6. [Driver APIs](#driver-apis)
7. [Route APIs](#route-apis)
8. [Bus APIs](#bus-apis)
9. [Route Stop APIs](#route-stop-apis)
10. [Student APIs](#student-apis)
11. [Trip APIs](#trip-apis)
12. [Tracking & Proximity APIs](#tracking--proximity-apis)
13. [Class & Promotion APIs](#class--promotion-apis)
14. [Notification History APIs](#notification-history-apis)
15. [Mobile App Versioning APIs](#mobile-app-versioning-apis)
16. [Error Handling APIs](#error-handling-apis)
17. [Database Table Models](#database-table-models)

---

## 🎯 Overview

**Base URL**: `http://api.selvagam.com/api/v1`
**API Version**: 1.0.0
**Authentication**: JWT Bearer Token

---

## 📊 Dashboard APIs
- `GET /dashboard/stats` - Comprehensive system statistics (counts, fleet, maintenance)

---

## 🔐 Authentication APIs

### 1. Split Login
**Endpoints**: 
- `POST /auth/admin/login`
- `POST /auth/parent/login`
- `POST /auth/driver/login`
**Description**: Separate login endpoints for different user types to ensure security and role isolation.

### 2. Logout & Tokens
- `POST /auth/logout` - Invalidate session and remove FCM token
- `POST /fcm-tokens` - Register/Update device token

### 3. Login Requests
- `POST /auth/login-requests/{id}/respond` - Approve/Reject new device login
- `GET /auth/login-requests/{id}` - Check status of pending request

### 4. Profile by Phone
**Endpoints**:
- `GET /auth/admin/profile/phone/{phone}`
- `GET /auth/parent/profile/phone/{phone}`
- `GET /auth/driver/profile/phone/{phone}`

---

## 👨‍💼 Admin APIs
- `GET /admins` - List all admins
- `GET /admins/phone-numbers/all` - Get all active admin phone numbers (flat list)
- `PATCH /admins/{id}/reset-password` - Reset password (Admin override)
- `PATCH /admins/{id}/reset-default-password` - Reset to auto-generated default

---

## 👨‍👩‍👧‍👦 Parent APIs
- `POST /parents` - Create parent
- `PUT /parents/{id}/fcm-token` - Update FCM token on login
- `GET /parents/fcm-tokens/all` - List all active parent tokens

---

## 🚗 Driver APIs
- `POST /drivers` - Create driver
- `POST /uploads/driver/{id}/photo` - Upload driver profile photo
- `GET /drivers/fcm-tokens/all` - List all active driver tokens

---

## 🚌 Bus APIs
- `POST /buses` - Create bus with RC/FC expiry tracking
- `POST /uploads/bus/{id}/rc-book` - Upload RC Book PDF/Image
- `POST /uploads/bus/{id}/fc-certificate` - Upload FC Certificate
- `PATCH /buses/{id}/driver` - Assign/Reassign driver to bus

---

## 🛣️ Route APIs
- `POST /routes` - Create route
- `GET /routes` - List all routes (with status filtering)
- `PUT /routes/{id}/status` - Activate/Deactivate route

---

## 🛑 Route Stop APIs
- `POST /route-stops` - Create stop (Automatic shifting of existing stops)
- `PUT /route-stops/{id}` - Update stop (Transactional reordering if order changes)
- `GET /route-stops/by-route/{route_id}/pickup-order` - Ordered list for pickup

---

## 🎓 Student APIs
- `POST /students` - Create student with Primary/Secondary parent assignment
- `PATCH /students/{id}/status` - Combined update for study and transport status
- `POST /students/{id}/switch-parents` - Swap Primary and Secondary parent roles
- `POST /uploads/student/{id}/photo` - Upload student photo

---

## 🗓️ Trip APIs
- `POST /trips` - Create trip (Morning/Evening)
- `GET /trips/ongoing/all` - List currently active trips

---

## 📡 Tracking & Proximity APIs
- `POST /bus-tracking/location` - Combined endpoint for:
    - Stop progression tracking
    - Trip auto-completion
    - Proximity alerts ("Approaching", "Arrived")
- `POST /trip/start` - Notify all parents on a route that the trip has started

---

## 🏫 Class & Promotion APIs
- `POST /students/bulk-upgrade-class` - Move all students from one class to another
- `POST /classes/promote-all` - Bulk increment all students' class (e.g., Class 9 → 10)
- `POST /classes/demote-all` - Bulk decrement all students' class (Admin rollback)

---

## 📜 Notification History APIs
- `POST /admin-parent-notifications` - Send & log notification
- `GET /admin-parent-notifications` - List all history
- `GET /admin-parent-notifications/student/{id}` - History for student
- `GET /admin-parent-notifications/parent/{id}` - History for parent
- `GET /admin-parent-notifications/admin/{id}` - History by admin

---

## 📱 Mobile App Versioning APIs
- `POST /check-app-version` - Check if app needs force/optional update
- `GET /app-versions` - List all configured versions (Admin)
- `POST /app-versions` - Create new version config

---

## ⚠️ Error Handling APIs
- `GET /error-handling` - List all system error logs
- `GET /error-handling/{id}` - Specific error details
- `DELETE /error-handling/{id}` - Remove error log

---

## 🗄️ Database Table Models (Key Fields)

### 1. Students Table
| Column | Type | Description |
|--------|------|-------------|
| student_id | UUID | Primary Key |
| parent_id | UUID | Primary Parent |
| s_parent_id | UUID | Secondary Parent (Nullable) |
| student_status | Enum | `CURRENT`, `ALUMNI`, `DISCONTINUED`, `LONG_ABSENT` |
| transport_status | Enum | `ACTIVE`, `INACTIVE` |

### 2. Buses Table
| Column | Type | Description |
|--------|------|-------------|
| status | Enum | `ACTIVE`, `INACTIVE`, `MAINTENANCE`, `SCRAP`, `SPARE` |
| rc_expiry_date | Date | Registration expiry |
| fc_expiry_date | Date | Fitness certificate expiry |

---

**Interactive Documentation**:
- [Swagger UI](http://api.selvagam.com/docs)
- [ReDoc](http://api.selvagam.com/redoc)

