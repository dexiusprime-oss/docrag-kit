# Deployment Guide

## Production Deployment

### Prerequisites

- Ubuntu 22.04 LTS server
- Nginx 1.24+
- PHP 8.2 with FPM
- PostgreSQL 15
- Redis 7.0
- Supervisor for queue workers

### Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install PHP 8.2
sudo add-apt-repository ppa:ondrej/php
sudo apt install php8.2-fpm php8.2-pgsql php8.2-redis php8.2-xml php8.2-mbstring

# Install PostgreSQL
sudo apt install postgresql-15

# Install Redis
sudo apt install redis-server

# Install Nginx
sudo apt install nginx
```

### Application Deployment

```bash
# Clone repository
cd /var/www
git clone https://github.com/example/ecommerce-platform.git
cd ecommerce-platform

# Install dependencies
composer install --no-dev --optimize-autoloader

# Setup environment
cp .env .env.local
# Edit .env.local with production values

# Run migrations
php bin/console doctrine:migrations:migrate --no-interaction

# Clear cache
php bin/console cache:clear --env=prod

# Set permissions
sudo chown -R www-data:www-data var/
sudo chmod -R 775 var/
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/ecommerce-platform/public;

    location / {
        try_files $uri /index.php$is_args$args;
    }

    location ~ ^/index\.php(/|$) {
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
        fastcgi_split_path_info ^(.+\.php)(/.*)$;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        fastcgi_param DOCUMENT_ROOT $realpath_root;
        internal;
    }

    location ~ \.php$ {
        return 404;
    }
}
```

### Queue Workers with Supervisor

```ini
[program:messenger-consume]
command=php /var/www/ecommerce-platform/bin/console messenger:consume async --time-limit=3600
user=www-data
numprocs=2
autostart=true
autorestart=true
process_name=%(program_name)s_%(process_num)02d
```

### SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com
```

## Docker Deployment

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:80"
    environment:
      DATABASE_URL: postgresql://user:pass@db:5432/ecommerce
      REDIS_URL: redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ecommerce
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - db_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  db_data:
```

Deploy with:
```bash
docker-compose up -d
```

## Monitoring

- **Application Logs**: `/var/www/ecommerce-platform/var/log/`
- **Nginx Logs**: `/var/log/nginx/`
- **PHP-FPM Logs**: `/var/log/php8.2-fpm.log`

Use tools like:
- Sentry for error tracking
- New Relic for performance monitoring
- Prometheus + Grafana for metrics
