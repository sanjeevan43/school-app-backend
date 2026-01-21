# 🌐 Setup School API on Subdomain

## Option 1: Use school.cholacabs.in (Recommended)

### Update nginx configuration:
```bash
cat > /etc/nginx/sites-available/school-api << 'EOF'
server {
    listen 80;
    server_name school.cholacabs.in;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable the site
ln -sf /etc/nginx/sites-available/school-api /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

## Option 2: Use api.cholacabs.in/school path

### Update nginx to add school path:
```bash
# Edit existing cholacabs config
nano /etc/nginx/sites-available/cholacabs

# Add this location block:
location /school/ {
    proxy_pass http://127.0.0.1:8000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## 🚀 Your School API URLs:

### If using subdomain (Option 1):
- **API Base**: https://school.cholacabs.in/api/v1
- **Swagger UI**: https://school.cholacabs.in/docs
- **ReDoc**: https://school.cholacabs.in/redoc

### If using path (Option 2):
- **API Base**: https://api.cholacabs.in/school/api/v1
- **Swagger UI**: https://api.cholacabs.in/school/docs
- **ReDoc**: https://api.cholacabs.in/school/redoc

## 📝 DNS Setup (if using subdomain):
Add this DNS record in your domain panel:
```
Type: A
Name: school
Value: 72.62.196.30
TTL: 300
```

## 🧪 Test Commands:

### For subdomain:
```bash
curl https://school.cholacabs.in/
curl https://school.cholacabs.in/docs
```

### For path:
```bash
curl https://api.cholacabs.in/school/
curl https://api.cholacabs.in/school/docs
```