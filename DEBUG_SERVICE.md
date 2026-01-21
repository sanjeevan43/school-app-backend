# 🔧 Debug and Fix School API Service

## Step 1: Check service status
```bash
systemctl status school-api
```

## Step 2: Check if service file exists and is correct
```bash
cat /etc/systemd/system/school-api.service
```

## Step 3: Check if app directory and files exist
```bash
ls -la /var/www/selvagam_school_app/
ls -la /var/www/selvagam_school_app/main.py
```

## Step 4: Test manual start
```bash
cd /var/www/selvagam_school_app
source venv/bin/activate
python main.py
```

## Step 5: If manual works, fix service
```bash
# Create correct service file
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

# Reload and start
systemctl daemon-reload
systemctl enable school-api
systemctl start school-api
```

## Step 6: Check logs if still failing
```bash
journalctl -u school-api -f
```

## Step 7: Quick test without systemd
```bash
cd /var/www/selvagam_school_app
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8001
```

## 🚀 Alternative: Run directly
```bash
# Navigate to app
cd /var/www/selvagam_school_app

# Activate environment
source venv/bin/activate

# Run directly on port 8001
python -c "
import uvicorn
from main import app
uvicorn.run(app, host='0.0.0.0', port=8001)
"
```