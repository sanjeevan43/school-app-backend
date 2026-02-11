#!/bin/bash
# Quick server update script
# This script pulls the latest code and restarts the service

echo "=== Updating School API Server ==="

# Navigate to project directory
cd /var/www/projects/client_side/selvegam_school || exit 1

# Stop the service
echo "Stopping school-api service..."
sudo systemctl stop school-api

# Pull latest code
echo "Pulling latest code from GitHub..."
git pull origin main

# Restart the service
echo "Starting school-api service..."
sudo systemctl start school-api

# Wait a moment for service to start
sleep 2

# Check status
echo ""
echo "=== Service Status ==="
sudo systemctl status school-api --no-pager

echo ""
echo "=== Recent Logs ==="
sudo journalctl -u school-api -n 20 --no-pager
