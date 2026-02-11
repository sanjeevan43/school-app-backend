# Deployment Fix Guide

## Problem
The school-api service is failing because the server has outdated code structure. The recent refactoring reorganized files into `app/` subdirectories, but the server still has the old structure.

## Solution Steps

### 1. Connect to Server and Navigate to Project
```bash
ssh sanjeevan@srv1308879
cd /var/www/projects/client_side/selvegam_school
```

### 2. Stop the Service
```bash
sudo systemctl stop school-api
```

### 3. Backup Current Code (Optional but Recommended)
```bash
cp -r /var/www/projects/client_side/selvegam_school /var/www/projects/client_side/selvegam_school_backup_$(date +%Y%m%d_%H%M%S)
```

### 4. Pull Latest Code from Git
```bash
# If using git
git pull origin main  # or master, depending on your branch name

# OR if you need to force update
git fetch --all
git reset --hard origin/main
```

### 5. Verify the New Structure
```bash
ls -la app/
ls -la app/core/
ls -la app/api/
ls -la app/services/
```

You should see:
- `app/__init__.py`
- `app/core/__init__.py`
- `app/core/config.py`
- `app/core/database.py`
- `app/api/__init__.py`
- `app/api/routes.py`
- `app/services/__init__.py`

### 6. Update Dependencies (if requirements.txt changed)
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 7. Check Environment Variables
```bash
cat .env
```

Ensure it has all required variables:
- DB_HOST
- DB_USER
- DB_PASSWORD
- DB_NAME
- SECRET_KEY

### 8. Test the Application Manually
```bash
source venv/bin/activate
python main.py
```

Press `Ctrl+C` if it starts successfully, then proceed to step 9.

If you see errors, check:
- Missing `__init__.py` files in app directories
- Import errors in the code
- Database connectivity

### 9. Restart the Service
```bash
sudo systemctl start school-api
```

### 10. Check Service Status
```bash
sudo systemctl status school-api
```

Should show: `Active: active (running)`

### 11. View Logs if Still Failing
```bash
# View recent logs
sudo journalctl -u school-api -n 50 --no-pager

# Or follow logs in real-time
sudo journalctl -u school-api -f
```

## Common Issues and Solutions

### Issue 1: ImportError for app.core.config
**Solution:** Ensure `app/__init__.py` and `app/core/__init__.py` exist

### Issue 2: Database Connection Error
**Solution:** Verify .env file has correct database credentials

### Issue 3: Permission Issues
**Solution:** 
```bash
sudo chown -R sanjeevan:sanjeevan /var/www/projects/client_side/selvegam_school
chmod -R 755 /var/www/projects/client_side/selvegam_school
```

### Issue 4: Port Already in Use
**Solution:**
```bash
# Find process using port 8000
sudo lsof -i :8000
# Kill the process
sudo kill -9 <PID>
```

## If Git is Not Set Up

If the code is not in a git repository, you'll need to manually upload the updated code:

### Option A: Using SCP from your Windows machine
```powershell
# From Windows PowerShell
scp -r C:\HS\school_app\school-app-backend\* sanjeevan@srv1308879:/var/www/projects/client_side/selvegam_school/
```

### Option B: Using rsync
```bash
rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '.git' C:/HS/school_app/school-app-backend/ sanjeevan@srv1308879:/var/www/projects/client_side/selvegam_school/
```

## Quick Check Script

Create this script on the server to quickly diagnose issues:

```bash
#!/bin/bash
echo "=== Checking School API Status ==="
echo ""
echo "1. Service Status:"
sudo systemctl status school-api --no-pager
echo ""
echo "2. Python Version:"
/var/www/projects/client_side/selvegam_school/venv/bin/python --version
echo ""
echo "3. Main.py exists:"
ls -lh /var/www/projects/client_side/selvegam_school/main.py
echo ""
echo "4. App structure:"
ls -lh /var/www/projects/client_side/selvegam_school/app/
echo ""
echo "5. Recent logs:"
sudo journalctl -u school-api -n 20 --no-pager
```

Save as `check_api.sh`, make executable with `chmod +x check_api.sh`, then run `./check_api.sh`
