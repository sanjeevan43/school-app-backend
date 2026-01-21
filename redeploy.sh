#!/bin/bash
# Quick Redeploy Script for Hostinger

echo "🔄 Redeploying School Transport API..."

# Stop existing service
systemctl stop school-api

# Backup current deployment
cp -r /var/www/school-api /var/www/school-api-backup-$(date +%Y%m%d-%H%M%S)

# Navigate to app directory
cd /var/www/school-api

# Activate virtual environment
source venv/bin/activate

# Update dependencies if needed
pip install --upgrade fastapi uvicorn pymysql pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] python-multipart email-validator

# Restart services
systemctl start school-api
systemctl restart nginx

# Check status
echo "✅ Checking service status..."
systemctl status school-api --no-pager -l

echo "🌐 API is live at: http://72.62.196.30"
echo "📖 Swagger UI: http://72.62.196.30/docs"