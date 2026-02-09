#!/bin/bash
# Setup Notification API to run 24/7 with systemd

echo "=== Setting up Notification API for 24/7 operation ==="

# Step 1: Check if main.py exists and what port it uses
echo ""
echo "Step 1: Checking your main.py file..."
if [ -f "main.py" ]; then
    echo "✓ main.py found"
    echo "Current main.py content:"
    cat main.py
else
    echo "✗ main.py not found. Please create it first."
    exit 1
fi

# Step 2: Create systemd service file
echo ""
echo "Step 2: Creating systemd service..."
sudo tee /etc/systemd/system/selvegam-notification.service > /dev/null << 'EOF'
[Unit]
Description=Selvegam School Notification API - FastAPI Application
After=network.target mysql.service

[Service]
Type=simple
User=sanjeevan
Group=sanjeevan
WorkingDirectory=/var/www/projects/client_side/selvegam_school/selvegam_school_notification
Environment="PATH=/var/www/projects/client_side/selvegam_school/selvegam_school_notification/venv/bin"
ExecStart=/var/www/projects/client_side/selvegam_school/selvegam_school_notification/venv/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "✓ Service file created at /etc/systemd/system/selvegam-notification.service"

# Step 3: Reload systemd
echo ""
echo "Step 3: Reloading systemd..."
sudo systemctl daemon-reload
echo "✓ Systemd reloaded"

# Step 4: Enable service
echo ""
echo "Step 4: Enabling service to start on boot..."
sudo systemctl enable selvegam-notification.service
echo "✓ Service enabled"

# Step 5: Start service
echo ""
echo "Step 5: Starting service..."
sudo systemctl start selvegam-notification.service
echo "✓ Service started"

# Step 6: Check status
echo ""
echo "Step 6: Checking service status..."
sudo systemctl status selvegam-notification.service

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Your API is now running 24/7!"
echo ""
echo "Useful commands:"
echo "  Check status:  sudo systemctl status selvegam-notification.service"
echo "  View logs:     sudo journalctl -u selvegam-notification.service -f"
echo "  Restart:       sudo systemctl restart selvegam-notification.service"
echo "  Stop:          sudo systemctl stop selvegam-notification.service"
echo ""
