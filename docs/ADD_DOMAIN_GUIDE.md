# 🌐 Adding api.selvagam.in Domain Guide (Hostinger VPS)

Since you are using **Hostinger**, follow these specific steps to point your custom subdomain (`api.selvagam.in`) to your VPS.

---

## 🔍 Troubleshooting DNS Propagation
If `ping api.selvagam.in` fails with **"Name or service not known"** after 30 minutes, check these common issues:

### 1. Check for "Double Domain" Mistake
Sometimes, if you type the full `api.selvagam.in` in the "Name" field, it actually creates `api.selvagam.in.selvagam.in`.
*   **Test this**: Run `ping api.selvagam.in.selvagam.in` in your terminal.
*   **Fix**: Edit the DNS record in Hostinger. Change **Name** from `api.selvagam.in` to just `api`.

### 2. Check Nameservers
Your DNS changes only work if your domain is using Hostinger's nameservers.
*   In Hostinger, go to **Domains** > **selvagam.in**.
*   Look for **Nameservers**. They should look like `ns1.dns-parking.com` or `ns1.hostinger.com`.
*   If they point to another service (like Cloudflare or GoDaddy), you must add the "A Record" **IN THAT SERVICE**, not in Hostinger.

### 3. Check Root Domain
Does the main domain work?
*   Run `ping selvagam.in`.
*   If this fails too, your domain registration might be inactive or nameservers are broken.

---

## ✅ Step 1: Hostinger DNS Configuration
You need to point the subdomain `api` to your VPS IP address (`72.61.250.191`).

1.  **Log in** to your [Hostinger hPanel](https://hpanel.hostinger.com/).
2.  Go to **Domains** and find `selvagam.in`.
3.  Click on **"DNS / Nameservers"**.
4.  Scroll down to the **"Manage DNS records"** section.
5.  Add a new record with these details:
    *   **Type**: `A`
    *   **Name**: `api` (Ensure you type ONLY `api`, not the full domain)
    *   **Points to**: `72.61.250.191` (Your VPS IP)
    *   **TTL**: `14400` (default is fine)

6.  Click **Add Record**.

---

## 🛠️ Step 2: VPS Nginx Configuration
Now you need to tell your server to accept traffic for `api.selvagam.in`.

### 1. Connect to your VPS
Open your terminal (PowerShell or Command Prompt) and SSH into your server:
```bash
ssh sanjeevan@72.61.250.191
```

### 2. Create the Nginx config file
```bash
sudo nano /etc/nginx/sites-available/api.selvagam.in
```

### 3. Add the configuration
Paste the following code. This tells Nginx to listen for `api.selvagam.in` and forward it to your Python app running on port **8080**.

```nginx
server {
    server_name api.selvagam.in;

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

*Press `Ctrl+X`, then `Y`, then `Enter` to save and exit.*

### 4. Enable the site
Link the new configuration to the enabled sites folder:
```bash
sudo ln -sf /etc/nginx/sites-available/api.selvagam.in /etc/nginx/sites-enabled/
```

### 5. Test and Reload Nginx
Check for typing mistakes:
```bash
sudo nginx -t
```
*(If you see "successful", proceed. If failed, check the file in Step 2 again).*

Reload Nginx to apply changes:
```bash
sudo systemctl reload nginx
```

---

## 🔒 Step 3: SSL Certificate (HTTPS)
Secure your API with a free SSL certificate using Certbot (Hostinger VPS templates usually come with this, or you can install it).

Run this command:
```bash
sudo certbot --nginx -d api.selvagam.in
```

1.  It will ask for your email (if not already set).
2.  It will ask to agree to terms (Type `Y`).
3.  **Important**: It will ask about redirecting HTTP to HTTPS. Choose **Option 2** (Redirect) to force secure connections.

---

## 🚀 Step 4: Verify
1.  Wait a few minutes for DNS to propagate.
2.  Open your browser and visit: **[https://api.selvagam.in/docs](https://api.selvagam.in/docs)**
3.  You should see your Swagger UI with the green lock icon (HTTPS).
