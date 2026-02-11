# School Transport Management API

A comprehensive REST API for managing school transportation, including students, parents, drivers, buses, routes, and real-time tracking.

## 📁 Project Structure

```
school-app-backend/
├── app/
│   ├── __init__.py
│   ├── api/                    # API endpoints and data models
│   │   ├── __init__.py
│   │   ├── routes.py          # All API route definitions
│   │   └── models.py          # Pydantic models and schemas
│   ├── core/                   # Core utilities and configuration
│   │   ├── __init__.py
│   │   ├── auth.py            # JWT authentication
│   │   ├── config.py          # Application configuration
│   │   ├── database.py        # Database connection and queries
│   │   └── encryption.py      # Data encryption utilities
│   └── services/               # Business logic services
│       ├── __init__.py
│       ├── bus_tracking.py    # Real-time bus tracking service
│       └── cascade_updates.py # Cascade update operations
├── docs/                       # Documentation files
│   ├── ADD_DOMAIN_GUIDE.md
│   ├── API_DOCUMENTATION.md
│   ├── API_FIXES_SUMMARY.md
│   ├── COMPLETE_API_DOCUMENTATION.md
│   ├── DEPLOY_SECOND_API_GUIDE.md
│   ├── School_Transport_API_Docs.docx
│   └── School_Transport_API_Docs.pdf
├── scripts/                    # Deployment and utility scripts
│   └── setup_notification_service.sh
├── sql/                        # SQL migration scripts  
│   ├── schema.sql
│   └── add_long_absent_status.sql
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file

```

## 🚀 Features

### Core Entities
- **Admins**: System administrators
- **Parents**: Student guardians with FCM push notifications
- **Drivers**: Bus drivers with real-time tracking
- **Students**: Student transport management
- **Buses**: Fleet management with status tracking
- **Routes**: Route and stop management
- **Trips**: Daily trip tracking

### Status Management
- **Student Status**: CURRENT, ALUMNI, DISCONTINUED, LONG_ABSENT
- **Transport Status**: ACTIVE, TEMP_STOP, CANCELLED
- **Bus Status**: ACTIVE, INACTIVE, MAINTENANCE, SCRAP, SPARE
- **Driver Status**: ACTIVE, INACTIVE, SUSPENDED, RESIGNED

### Advanced Features
- JWT-based authentication
- Real-time bus tracking
- FCM push notifications
- Cascade updates across related entities
- Data encryption
- Comprehensive error handling

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/sanjeevan43/school-app-backend.git
cd school-app-backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\\Scripts\\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Setup database**
```bash
mysql -u your_user -p your_database < sql/schema.sql
mysql -u your_user -p your_database < sql/add_long_absent_status.sql
```

## 🏃 Running the API

### Development Mode
```bash
python main.py
```

### Production Mode (with systemd)
See `docs/DEPLOY_SECOND_API_GUIDE.md` for production deployment instructions.

## 📚 API Documentation

Once running, access interactive documentation at:
- **Swagger UI**: https://api.selvagam.com/docs
- **ReDoc**: https://api.selvagam.com/redoc

## 🔑 Environment Variables

```env
# Database
DB_HOST=your_host
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=school_DB

# JWT
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS
ALLOWED_ORIGINS=["*"]

# FCM
FCM_SERVER_KEY=your_fcm_key
```

## 🔧 Tech Stack

- **Framework**: FastAPI
- **Database**: MySQL
- **Authentication**: JWT
- **Notifications**: FCM (Firebase Cloud Messaging)
- **Encryption**: Fernet (symmetric encryption)

## 📖 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Universal login for all user types
- `GET /api/v1/auth/profile` - Get user profile by phone

### Key Endpoints
- `/api/v1/admins` - Admin management
- `/api/v1/parents` - Parent management with FCM tokens
- `/api/v1/drivers` - Driver management
- `/api/v1/students` - Student management with status filters
- `/api/v1/buses` - Bus fleet management
- `/api/v1/routes` - Route and stop management
- `/api/v1/trips` - Daily trip tracking
- `/api/v1/bus-tracking` - Real-time bus tracking

## 🛠️ Development

### Code Organization
- **app/api/**: All API routes and data models
- **app/core/**: Configuration, auth, database, encryption
- **app/services/**: Business logic (tracking, cascades)
- **docs/**: All documentation
- **sql/**: Database migration scripts
- **scripts/**: Deployment and utility scripts

### Adding New Endpoints
1. Define models in `app/api/models.py`
2. Add routes in `app/api/routes.py`
3. Update documentation

## 📝 License

This project is proprietary software for school transport management.

## 👥 Support

For API support, contact: admin@school.com