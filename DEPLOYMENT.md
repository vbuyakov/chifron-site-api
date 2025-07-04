# Chifron Voice API - Deployment Guide

## Prerequisites
- Linux server (Ubuntu/Debian recommended)
- Docker and Docker Compose installed
- Git installed
- Ports 80, 443, and 5000 open in your firewall

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url> /opt/voiceapi
cd /opt/voiceapi
```

### 2. Configure Environment

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your configuration:
   ```bash
   nano .env
   ```

### 3. Set Up SSL (Recommended)

1. Install Nginx and Certbot:
   ```bash
   sudo apt update
   sudo apt install -y nginx certbot python3-certbot-nginx
   ```

2. Configure Nginx with your domain:
   ```bash
   sudo nano /etc/nginx/sites-available/yourdomain.com
   ```
   
   Example configuration:
   ```nginx
   server {
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. Enable the site and get SSL certificate:
   ```bash
   sudo ln -s /etc/nginx/sites-available/yourdomain.com /etc/nginx/sites-enabled/
   sudo certbot --nginx -d yourdomain.com
   ```

### 4. Deploy with Docker Compose

```bash
# Build and start the application
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Updating the Application

```bash
# Pull the latest changes
git pull

# Rebuild and restart the containers
docker-compose -f docker-compose.prod.yml up -d --build
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Port the application runs on | `5000` |
| `CONFIG_PATH` | Path to the config file | `/app/configs/config.json` |
| `DOCKER_CONTAINER` | Set to `true` when running in Docker | `false` |

## Troubleshooting

### View Logs
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

### Check Running Containers
```bash
docker ps
```

### Rebuild from Scratch
```bash
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
```

# Clone your repository
git clone <your-repository-url> .
```

### 2.2 Configure Environment

```bash
cp .env.example .env
nano .env
```

### 2.3 Build and Start Services

```bash
# Make deployment script executable
chmod +x deploy.sh
chmod +x deploy-production.sh

# Build and start the API service
docker-compose -f docker-compose.prod.yml up -d --build

# Verify the container is running
docker ps
```

### 2.4 Verify API Health

```bash
# Check if the API is responding (default port is 5001)
curl http://localhost:5001/api/health
```

If you need to use a different port, set the `CHIFRON_API_PORT` environment variable:

```bash
export CHIFRON_API_PORT=8702  # Or your preferred port
docker-compose -f docker-compose.prod.yml up -d --build
```

## 3. Nginx Configuration

### 3.1 Copy and Customize Nginx Configuration Template

**Note**: A template file `nginx/yourdomain.com.conf.template` is provided. You need to copy it and replace `yourdomain.com` with your actual domain name.

```bash
# Copy and customize the Nginx configuration template
sudo cp nginx/yourdomain.com.conf.template /etc/nginx/sites-available/yourdomain.com.conf
sudo sed -i 's/yourdomain.com/your-actual-domain.com/g' /etc/nginx/sites-available/yourdomain.com.conf

# Create a symlink to enable the site
sudo ln -sf /etc/nginx/sites-available/yourdomain.com.conf /etc/nginx/sites-enabled/

# Test the configuration
sudo nginx -t

# Reload Nginx to apply changes
sudo systemctl reload nginx
```

### 3.2 Verify Nginx Configuration

Make sure your Nginx configuration includes the following proxy settings:

```nginx
location / {
    proxy_pass http://127.0.0.1:8702;  # Matches the port in docker-compose.prod.yml
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # WebSocket support
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    
    # Timeouts
    proxy_read_timeout 1m;
    proxy_connect_timeout 1m;
}
```

## 4. SSL Setup

### 4.1 Install SSL Certificate

1. First, stop Nginx to free up port 80:
   ```bash
   sudo systemctl stop nginx
   ```

2. Install Certbot if not already installed:
   ```bash
   sudo apt update
   sudo apt install -y certbot
   ```

3. Generate the SSL certificate using standalone mode (this will temporarily use port 80):
   ```bash
   sudo certbot certonly --standalone -d yourdomain.com --non-interactive --agree-tos -m your-email@example.com --preferred-challenges http
   ```

4. Verify the certificate was created:
   ```bash
   sudo ls -l /etc/letsencrypt/live/yourdomain.com/
   ```
   You should see `fullchain.pem` and `privkey.pem` files.

5. Start Nginx again:
   ```bash
   sudo systemctl start nginx
   ```

6. Update Nginx configuration to use the SSL certificates (if not already configured):
   ```bash
   sudo nano /etc/nginx/sites-available/yourdomain.com.conf
   ```
   Ensure these lines exist in your server block:
   ```nginx
   ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
   ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
   include /etc/letsencrypt/options-ssl-nginx.conf;
   ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
   ```

### 4.2 Set Up Auto-Renewal

```bash
# Test the renewal process
sudo certbot renew --dry-run

# Add a cron job for auto-renewal
(sudo crontab -l 2>/dev/null; echo "0 0,12 * * * root python3 -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew -q") | sudo crontab -
```

## 5. Verification

### 5.1 Verify Application

```bash
# Check API health
curl http://localhost:5000/api/health  # Should return "OK"

# Check Nginx response
curl -I https://yourdomain.com   # Should return 200 OK
```

## 6. Maintenance

### 6.1 View Logs

```bash
# View all logs
docker-compose -f docker-compose.prod.yml logs -f

# View specific service logs
docker-compose -f docker-compose.prod.yml logs -f chifron-api
```

### 6.2 Update the Application

```bash
# Navigate to project directory
cd /srv/www/yourproject

# Pull latest changes
git pull origin main  # Or your branch

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build chifron-api
```

## 7. Troubleshooting

### 7.1 Common Issues

#### Containers not starting
```bash
# Check container status
docker ps -a

# View container logs
docker logs <container_id>
```

#### Nginx Issues
```bash
# Test Nginx configuration
sudo nginx -t

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

#### SSL Certificate Issues
```bash
# Check certificate status
sudo certbot certificates

# Manually renew certificates
sudo certbot renew --force-renewal
```

### 7.2 Getting Help
If you encounter any issues, please check the following:
1. All services are running: `docker ps`
2. No port conflicts: `sudo netstat -tuln | grep -E ':(80|443|5000)'`
3. Firewall allows necessary ports: `sudo ufw status`

For additional support, please contact your system administrator.

## Security Considerations

1. **Firewall**: Ensure your server's firewall allows ports 80, 443, and 22:
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

2. **Automatic updates**: Enable automatic security updates:
   ```bash
   sudo apt-get install -y unattended-upgrades
   sudo dpkg-reconfigure -plow unattended-upgrades
   ```

3. **Backup**: Set up regular backups of important data:
   ```bash
   # Add to /etc/crontab
0 3 * * * root tar -czf /backups/yourproject-$(date +\%Y\%m\%d).tar.gz /srv/www/yourproject
   ```
