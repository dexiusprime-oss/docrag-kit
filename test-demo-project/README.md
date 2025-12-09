# E-Commerce Platform

A modern e-commerce platform built with Symfony 6.4 and modern web technologies.

## Features

- **Product Catalog**: Browse and search products with advanced filtering
- **Shopping Cart**: Add products to cart with real-time updates
- **User Authentication**: Secure login and registration system
- **Order Management**: Track orders and view order history
- **Payment Integration**: Support for Stripe and PayPal
- **Admin Dashboard**: Manage products, orders, and users

## Tech Stack

- **Backend**: Symfony 6.4, PHP 8.2
- **Database**: PostgreSQL 15
- **Cache**: Redis
- **Queue**: RabbitMQ
- **Frontend**: Twig templates with Alpine.js
- **API**: RESTful API with API Platform

## Installation

```bash
# Clone repository
git clone https://github.com/example/ecommerce-platform.git

# Install dependencies
composer install
npm install

# Setup database
php bin/console doctrine:database:create
php bin/console doctrine:migrations:migrate

# Start development server
symfony server:start
```

## Configuration

Copy `.env` to `.env.local` and configure:

```env
DATABASE_URL="postgresql://user:pass@localhost:5432/ecommerce"
REDIS_URL="redis://localhost:6379"
STRIPE_SECRET_KEY="sk_test_..."
```

## Testing

```bash
# Run unit tests
php bin/phpunit

# Run integration tests
php bin/phpunit --testsuite=integration
```
