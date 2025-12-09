"""Sample documentation fixtures for testing."""

SAMPLE_README = """# Sample Project

This is a sample project for testing DocRAG Kit.

## Overview

The project demonstrates:
- Document indexing
- Semantic search
- Vector embeddings
- RAG (Retrieval-Augmented Generation)

## Installation

```bash
pip install docrag-kit
```

## Usage

1. Initialize: `docrag init`
2. Index: `docrag index`
3. Configure MCP: `docrag mcp-config`

## Features

### Feature 1: Quick Setup
Initialize RAG system with a single command.

### Feature 2: Universal
Works with any documentation format.

### Feature 3: MCP Integration
Seamless integration with Kiro AI.
"""

SAMPLE_API_DOC = """# API Documentation

## Authentication

All API requests require authentication using JWT tokens.

### Login Endpoint

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
  "expires_in": 3600
}
```

## Users API

### List Users

```http
GET /api/users?page=1&limit=20
Authorization: Bearer {token}
```

### Get User

```http
GET /api/users/{id}
Authorization: Bearer {token}
```

### Create User

```http
POST /api/users
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com"
}
```

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Validation failed"
  }
}
```

### Common Error Codes

- `UNAUTHORIZED` (401): Invalid or missing token
- `FORBIDDEN` (403): Insufficient permissions
- `NOT_FOUND` (404): Resource not found
- `VALIDATION_ERROR` (422): Invalid input data
"""

SAMPLE_DEPLOYMENT_DOC = """# Deployment Guide

## Prerequisites

- Ubuntu 22.04 LTS
- Python 3.10+
- PostgreSQL 15
- Redis 7.0

## Installation Steps

### 1. System Setup

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3.10 python3-pip postgresql redis-server
```

### 2. Application Setup

```bash
git clone https://github.com/example/project.git
cd project
pip install -r requirements.txt
```

### 3. Database Setup

```bash
createdb myproject
python manage.py migrate
```

### 4. Environment Configuration

Create `.env` file:

```env
DATABASE_URL=postgresql://user:pass@localhost/myproject
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
```

### 5. Start Services

```bash
# Start application
python manage.py runserver

# Start worker
celery -A myproject worker -l info
```

## Production Deployment

### Using Docker

```bash
docker-compose up -d
```

### Using Systemd

Create service file `/etc/systemd/system/myproject.service`:

```ini
[Unit]
Description=My Project
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/myproject
ExecStart=/usr/bin/python manage.py runserver

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable myproject
sudo systemctl start myproject
```

## Monitoring

- Application logs: `/var/log/myproject/`
- System metrics: Prometheus + Grafana
- Error tracking: Sentry
"""

SAMPLE_CONFIG_YAML = """project:
  name: Test Project
  type: general

llm:
  provider: openai
  embedding_model: text-embedding-3-small
  llm_model: gpt-4o-mini
  temperature: 0.3

indexing:
  directories:
    - .
  extensions:
    - .md
    - .txt
  exclude_patterns:
    - node_modules/
    - .git/
    - __pycache__/

chunking:
  chunk_size: 800
  chunk_overlap: 150

retrieval:
  top_k: 3

prompt:
  template: |
    You are a developer assistant. Answer based on this context:
    
    {context}
    
    Question: {question}
    
    Answer concisely:
"""


def create_sample_project(path):
    """
    Create a sample project structure for testing.
    
    Args:
        path: Path to create the project in
    
    Returns:
        Dictionary with paths to created files
    """
    from pathlib import Path
    
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    
    # Create documentation files
    readme_path = path / "README.md"
    readme_path.write_text(SAMPLE_README)
    
    api_path = path / "API.md"
    api_path.write_text(SAMPLE_API_DOC)
    
    deploy_path = path / "DEPLOYMENT.md"
    deploy_path.write_text(SAMPLE_DEPLOYMENT_DOC)
    
    # Create .docrag directory
    docrag_dir = path / ".docrag"
    docrag_dir.mkdir(exist_ok=True)
    
    config_path = docrag_dir / "config.yaml"
    config_path.write_text(SAMPLE_CONFIG_YAML)
    
    return {
        "readme": readme_path,
        "api": api_path,
        "deployment": deploy_path,
        "config": config_path,
        "docrag_dir": docrag_dir
    }
