# 🚌 School Transport Management API - Complete Endpoints List

**Base URL**: `http://localhost:8000/api/v1`

## 🔐 Authentication (4 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/admin/login` | Admin password login |
| `POST` | `/auth/send-otp` | Send OTP to parent/driver |
| `POST` | `/auth/verify-otp` | Verify OTP and login |
| `POST` | `/auth/resend-otp` | Resend OTP |

## 👨💼 Admins (6 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/admins` | Create admin |
| `GET` | `/admins` | Get all admins |
| `GET` | `/admins/me` | Get current admin |
| `GET` | `/admins/{id}` | Get admin by ID |
| `PUT` | `/admins/{id}` | Update admin |
| `DELETE` | `/admins/{id}` | Delete admin |

## 👨👩👧👦 Parents (6 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/parents` | Create parent |
| `GET` | `/parents` | Get all parents |
| `GET` | `/parents/me` | Get current parent |
| `GET` | `/parents/{id}` | Get parent by ID |
| `PUT` | `/parents/{id}` | Update parent |
| `DELETE` | `/parents/{id}` | Delete parent |

## 🚗 Drivers (6 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/drivers` | Create driver |
| `GET` | `/drivers` | Get all drivers |
| `GET` | `/drivers/available` | Get available drivers |
| `GET` | `/drivers/{id}` | Get driver by ID |
| `PUT` | `/drivers/{id}` | Update driver |
| `DELETE` | `/drivers/{id}` | Delete driver |

## 🛣️ Routes (5 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/routes` | Create route |
| `GET` | `/routes` | Get all routes |
| `GET` | `/routes/{id}` | Get route by ID |
| `PUT` | `/routes/{id}` | Update route |
| `DELETE` | `/routes/{id}` | Delete route |

## 🚌 Buses (5 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/buses` | Create bus |
| `GET` | `/buses` | Get all buses |
| `GET` | `/buses/{id}` | Get bus by ID |
| `PUT` | `/buses/{id}` | Update bus |
| `DELETE` | `/buses/{id}` | Delete bus |

## 🚏 Route Stops (5 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/route-stops` | Create route stop |
| `GET` | `/route-stops` | Get all route stops |
| `GET` | `/route-stops/{id}` | Get route stop by ID |
| `PUT` | `/route-stops/{id}` | Update route stop |
| `DELETE` | `/route-stops/{id}` | Delete route stop |

## 🎓 Students (6 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/students` | Create student |
| `GET` | `/students` | Get all students |
| `GET` | `/students/parent/{parent_id}` | Get students by parent |
| `GET` | `/students/{id}` | Get student by ID |
| `PUT` | `/students/{id}` | Update student |
| `DELETE` | `/students/{id}` | Delete student |

## 🚌 Trips (5 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/trips` | Create trip |
| `GET` | `/trips` | Get all trips |
| `GET` | `/trips/{id}` | Get trip by ID |
| `PUT` | `/trips/{id}` | Update trip |
| `DELETE` | `/trips/{id}` | Delete trip |

---

## 📊 Summary
- **Total Endpoints**: 48
- **POST**: 9 endpoints (Create operations)
- **GET**: 27 endpoints (Read operations)
- **PUT**: 8 endpoints (Update operations)
- **DELETE**: 8 endpoints (Delete operations)

## 🔗 Quick Links
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Base**: http://localhost:8000/api/v1