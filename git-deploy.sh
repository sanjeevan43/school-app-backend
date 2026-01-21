#!/bin/bash
# Automated Git Deployment Script

echo "🚀 Starting Git Deployment..."

# Stop API service
echo "⏹️ Stopping API service..."
systemctl stop school-api

# Pull latest code
echo "📥 Pulling latest code from Git..."
git pull origin main

# Activate virtual environment and update dependencies
echo "📦 Updating dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Start services
echo "▶️ Starting services..."
systemctl start school-api
systemctl restart nginx

# Check status
echo "✅ Checking deployment status..."
sleep 3
systemctl status school-api --no-pager -l

# Test API
echo "🧪 Testing API..."
curl -s http://72.62.196.30/health

echo ""
echo "🎉 Git Deployment Complete!"
echo "🌐 API: http://72.62.196.30/api/v1"
echo "📖 Docs: http://72.62.196.30/docs"