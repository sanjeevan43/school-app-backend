# 🚀 Git Deployment Commands - Step by Step

## Step 1: Push Code to Git (Local Machine)
```bash
cd "c:\HS\school_app\API's"
git add .
git commit -m "Updated API code"
git push origin main
```

## Step 2: Connect to Hostinger Server
```bash
ssh root@72.62.196.30
```

## Step 3: Navigate to App Directory
```bash
cd /var/www/school-api
```

## Step 4: Stop API Service
```bash
systemctl stop school-api
```

## Step 5: Pull Latest Code from Git
```bash
git pull origin main
```

## Step 6: Activate Virtual Environment
```bash
source venv/bin/activate
```

## Step 7: Install/Update Dependencies
```bash
pip install -r requirements.txt
```

## Step 8: Start API Service
```bash
systemctl start school-api
```

## Step 9: Restart Nginx
```bash
systemctl restart nginx
```

## Step 10: Check Status
```bash
systemctl status school-api
curl http://72.62.196.30/health
```

## 🔄 One-Line Git Redeploy
```bash
systemctl stop school-api && git pull origin main && systemctl start school-api && systemctl restart nginx && echo "✅ Git Redeployed!"
```

## 📱 Test Your Deployment
- Health: http://72.62.196.30/health
- Swagger: http://72.62.196.30/docs
- API: http://72.62.196.30/api/v1