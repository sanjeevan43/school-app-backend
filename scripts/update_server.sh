#!/bin/bash

# Server Update Script
# Run this on your server after pulling new code

echo "📦 Pulling latest code..."
cd /var/www/projects/client_side/selvegam_school
git pull origin main

echo "🗄️ Updating database schema..."
mysql -u u591840779_selvagam_user -p u591840779_selvagam_db < sql/add_long_absent_status.sql

echo "🔄 Restarting service..."
sudo systemctl restart school-api

echo "✅ Checking service status..."
sudo systemctl status school-api --no-pager

echo ""
echo "🎉 Update complete!"
echo "Check API at: https://api.selvagam.com/docs"
