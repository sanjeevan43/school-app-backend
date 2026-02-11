# 🚀 Deploy Second API on Same Server - Complete Guide

## Current Setup
- **Server IP**: 72.61.250.191
- **Existing API**: School Transport API (Port 8080)
- **Current Path**: /var/www/projects/client_side/selvegam_school
- **New API**: Will use a different port (e.g., 8081)

---

## Step 1: Create Project Directory

```bash
# Navigate to projects directory
cd /var/www/projects/client_side

# Create new folder for your second API
sudo mkdir -p selvegam_school_api2
cd selvegam_school_api2

# Set proper ownership
sudo chown -R sanjeevan:sanjeevan /var/www/projects/client_side/selvegam_school_api2
```

---

## Step 2: Clone Your Git Repository

```bash
# Clone your repository (replace with your actual git URL)
git clone https://github.com/yourusername/your-repo-name.git .

# OR if you already have the code elsewhere, copy it
# cp -r /path/to/your/code/* .
```

---

## Step 3: Set Up Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables

```bash
# Create .env file
nano .env
```

**Add your configuration** (modify as needed):
```env
DB_HOST=your_mysql_host
DB_PORT=3306
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
SECRET_KEY=your-secret-key-change-in-production
PORT=8081
```

**Save and exit**: `Ctrl+X`, then `Y`, then `Enter`

---

## Step 5: Update main.py to Use New Port

```bash
# Edit your main.py file
nano main.py
```

**Make sure it includes**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8081))  # Default to 8081
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
```

---

## Step 6: Test the API Manually

```bash
# Make sure you're in the project directory
cd /var/www/projects/client_side/selvegam_school_api2

# Activate virtual environment
source venv/bin/activate

# Run the API
python main.py
```

**Test in another terminal**:
```bash
curl http://localhost:8081/docs
```

If it works, press `Ctrl+C` to stop it.

---

## Step 7: Create Systemd Service for Auto-Start

```bash
# Create service file
sudo nano /etc/systemd/system/selvegam-api2.service
```

**Add this configuration**:
```ini
[Unit]
Description=Selvegam School API 2 - FastAPI Application
After=network.target mysql.service

[Service]
Type=simple
User=sanjeevan
Group=sanjeevan
WorkingDirectory=/var/www/projects/client_side/selvegam_school_api2
Environment="PATH=/var/www/projects/client_side/selvegam_school_api2/venv/bin"
ExecStart=/var/www/projects/client_side/selvegam_school_api2/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Save and exit**: `Ctrl+X`, then `Y`, then `Enter`

---

## Step 8: Enable and Start the Service

```bash
# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable selvegam-api2.service

# Start the service
sudo systemctl start selvegam-api2.service

# Check status
sudo systemctl status selvegam-api2.service
```

---

## Step 9: Configure Nginx Reverse Proxy

```bash
# Edit Nginx configuration
sudo nano /etc/nginx/sites-available/default
```

**Add this location block** (inside the existing `server` block):
```nginx
# API 2 - Port 8081
location /api2/ {
    proxy_pass http://localhost:8081/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

**Test Nginx configuration**:
```bash
sudo nginx -t
```

**Reload Nginx**:
```bash
sudo systemctl reload nginx
```

---

## Step 10: Configure Firewall (if needed)

```bash
# Allow port 8081 through firewall
sudo ufw allow 8081/tcp

# Check firewall status
sudo ufw status
```

---

## Step 11: Test Your APIs

### Test API 1 (Existing - Port 8080):
```bash
curl http://72.61.250.191:8080/docs
# OR via Nginx
curl http://72.61.250.191/api/v1/docs
```

### Test API 2 (New - Port 8081):
```bash
curl http://72.61.250.191:8081/docs
# OR via Nginx
curl http://72.61.250.191/api2/docs
```

---

## Useful Commands for Management

### Check Service Status
```bash
sudo systemctl status selvegam-api2.service
```

### View Logs
```bash
# View service logs
sudo journalctl -u selvegam-api2.service -f

# View last 100 lines
sudo journalctl -u selvegam-api2.service -n 100
```

### Restart Service
```bash
sudo systemctl restart selvegam-api2.service
```

### Stop Service
```bash
sudo systemctl stop selvegam-api2.service
```

### Update Code from Git
```bash
cd /var/www/projects/client_side/selvegam_school_api2
git pull origin main
sudo systemctl restart selvegam-api2.service
```

---

## Summary of URLs

| API | Direct Access | Via Nginx Proxy |
|-----|---------------|-----------------|
| API 1 (School Transport) | http://72.61.250.191:8080 | http://72.61.250.191/api/v1 |
| API 2 (New API) | http://72.61.250.191:8081 | http://72.61.250.191/api2 |

---

## Troubleshooting

### If API doesn't start:
```bash
# Check if port is already in use
sudo lsof -i :8081

# Check service logs
sudo journalctl -u selvegam-api2.service -n 50

# Check if virtual environment is correct
which python
# Should show: /var/www/projects/client_side/selvegam_school_api2/venv/bin/python
```

### If database connection fails:
```bash
# Test database connection
mysql -h your_host -u your_user -p your_database

# Check .env file
cat .env
```

### If Nginx returns 502 Bad Gateway:
```bash
# Check if API is running
sudo systemctl status selvegam-api2.service

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

---

## Quick Start Commands (Copy-Paste Ready)

```bash
# 1. Create directory
cd /var/www/projects/client_side
sudo mkdir -p selvegam_school_api2
sudo chown -R sanjeevan:sanjeevan selvegam_school_api2
cd selvegam_school_api2

# 2. Clone your repo (replace URL)
git clone YOUR_GIT_URL .

# 3. Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Create .env file (then edit it)
nano .env

# 5. Test manually
python main.py

# 6. Create systemd service (then add configuration)
sudo nano /etc/systemd/system/selvegam-api2.service

# 7. Enable and start
sudo systemctl daemon-reload
sudo systemctl enable selvegam-api2.service
sudo systemctl start selvegam-api2.service
sudo systemctl status selvegam-api2.service

# 8. Configure Nginx (add location block)
sudo nano /etc/nginx/sites-available/default
sudo nginx -t
sudo systemctl reload nginx

# Done! Test your API
curl http://72.61.250.191:8081/docs
```

---

**Need help? Check logs with:**
```bash
sudo journalctl -u selvegam-api2.service -f
```
