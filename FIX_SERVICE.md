# 🔧 Fix Missing Service - Run These Commands

## Step 1: Create the systemd service file
```bash
cat > /etc/systemd/system/school-api.service << EOF
[Unit]
Description=School Transport API
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/www/selvagam_school_app
Environment="PATH=/var/www/selvagam_school_app/venv/bin"
ExecStart=/var/www/selvagam_school_app/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

## Step 2: Configure nginx
```bash
cat > /etc/nginx/sites-available/school-api << EOF
server {
    listen 80;
    server_name 72.62.196.30;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
```

## Step 3: Enable nginx site
```bash
ln -sf /etc/nginx/sites-available/school-api /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
```

## Step 4: Enable and start services
```bash
systemctl daemon-reload
systemctl enable school-api
systemctl start school-api
systemctl restart nginx
```

## Step 5: Check status
```bash
systemctl status school-api
curl http://72.62.196.30/health
```

## 🚀 Quick Setup (Copy & Paste All)
```bash
# Create service
cat > /etc/systemd/system/school-api.service << 'EOF'
[Unit]
Description=School Transport API
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/www/selvagam_school_app
Environment="PATH=/var/www/selvagam_school_app/venv/bin"
ExecStart=/var/www/selvagam_school_app/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configure nginx
cat > /etc/nginx/sites-available/school-api << 'EOF'
server {
    listen 80;
    server_name 72.62.196.30;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable and start
ln -sf /etc/nginx/sites-available/school-api /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl daemon-reload
systemctl enable school-api
systemctl start school-api
systemctl restart nginx

# Test
systemctl status school-api
curl http://72.62.196.30/health
```