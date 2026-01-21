# 🔧 Setup School API on Different Port (IP Only)

## Configure School API on Port 8001

### 1. Update systemd service for different port:
```bash
cat > /etc/systemd/system/school-api.service << 'EOF'
[Unit]
Description=School Transport API
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/www/selvagam_school_app
Environment="PATH=/var/www/selvagam_school_app/venv/bin"
ExecStart=/var/www/selvagam_school_app/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

### 2. Create nginx config for port 8001:
```bash
cat > /etc/nginx/sites-available/school-api-8001 << 'EOF'
server {
    listen 8001;
    server_name 72.62.196.30;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
```

### 3. Enable and restart services:
```bash
ln -sf /etc/nginx/sites-available/school-api-8001 /etc/nginx/sites-enabled/
nginx -t
systemctl daemon-reload
systemctl restart school-api
systemctl restart nginx
```

### 4. Open firewall port:
```bash
ufw allow 8001
```

## 🌐 Your School API URLs (IP Only):
- **API Base**: http://72.62.196.30:8001/api/v1
- **Swagger UI**: http://72.62.196.30:8001/docs
- **ReDoc**: http://72.62.196.30:8001/redoc

## 🧪 Test Commands:
```bash
curl http://72.62.196.30:8001/
curl http://72.62.196.30:8001/docs
curl -X POST "http://72.62.196.30:8001/api/v1/admins" \
  -H "Content-Type: application/json" \
  -d '{"phone": 9876543210, "email": "admin@school.com", "name": "Admin", "password": "admin123", "dob": "1990-01-01"}'
```

## ⚡ Quick Setup Commands:
```bash
# Update service for port 8001
systemctl stop school-api
sed -i 's/--port 8000/--port 8001/g' /etc/systemd/system/school-api.service
systemctl daemon-reload
systemctl start school-api

# Allow port in firewall
ufw allow 8001

# Test
curl http://72.62.196.30:8001/docs
```