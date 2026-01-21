# 🔄 Quick Redeployment Commands

## 1. Connect to Server
```bash
ssh root@72.62.196.30
```

## 2. Upload New Code
```bash
# From your local machine (run this first)
scp -r "c:\HS\school_app\API's\*.py" root@72.62.196.30:/var/www/school-api/
scp "c:\HS\school_app\API's\.env" root@72.62.196.30:/var/www/school-api/
```

## 3. Restart Services (on server)
```bash
cd /var/www/school-api
systemctl restart school-api
systemctl restart nginx
```

## 4. Check Status
```bash
systemctl status school-api
curl http://72.62.196.30/health
```

## 🚀 One-Line Redeploy
```bash
systemctl stop school-api && systemctl start school-api && systemctl restart nginx && echo "✅ Redeployed!"
```

## 📱 Test Your API
- **Health**: http://72.62.196.30/health
- **Swagger**: http://72.62.196.30/docs
- **API**: http://72.62.196.30/api/v1