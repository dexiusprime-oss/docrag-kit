# API Documentation

## Authentication

All API requests require authentication using JWT tokens.

### Login

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "...",
  "expires_in": 3600
}
```

## Products API

### List Products

```http
GET /api/products?page=1&limit=20&category=electronics
Authorization: Bearer {token}
```

Response:
```json
{
  "data": [
    {
      "id": 1,
      "name": "Laptop Pro 15",
      "price": 1299.99,
      "category": "electronics",
      "stock": 45
    }
  ],
  "meta": {
    "total": 150,
    "page": 1,
    "per_page": 20
  }
}
```

### Get Product Details

```http
GET /api/products/{id}
Authorization: Bearer {token}
```

### Create Product (Admin only)

```http
POST /api/products
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "New Product",
  "description": "Product description",
  "price": 99.99,
  "category": "electronics",
  "stock": 100
}
```

## Orders API

### Create Order

```http
POST /api/orders
Authorization: Bearer {token}
Content-Type: application/json

{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ],
  "shipping_address": {
    "street": "123 Main St",
    "city": "New York",
    "zip": "10001"
  },
  "payment_method": "stripe"
}
```

### Get Order Status

```http
GET /api/orders/{id}
Authorization: Bearer {token}
```

Response:
```json
{
  "id": 123,
  "status": "processing",
  "total": 2599.98,
  "created_at": "2024-01-15T10:30:00Z",
  "items": [...]
}
```

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Validation failed",
    "details": {
      "email": ["Email is required"]
    }
  }
}
```

### Common Error Codes

- `UNAUTHORIZED` (401): Invalid or missing token
- `FORBIDDEN` (403): Insufficient permissions
- `NOT_FOUND` (404): Resource not found
- `VALIDATION_ERROR` (422): Invalid input data
- `RATE_LIMIT_EXCEEDED` (429): Too many requests
