"""Pytest configuration and shared fixtures."""

import pytest
import os
from pathlib import Path
from tests.fixtures.sample_docs import create_sample_project


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory."""
    return tmp_path


@pytest.fixture
def sample_project(tmp_path):
    """Create a sample project with documentation files."""
    return create_sample_project(tmp_path)


@pytest.fixture
def mock_openai_key(monkeypatch):
    """Mock OpenAI API key for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-for-testing")
    yield
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)


@pytest.fixture
def mock_google_key(monkeypatch):
    """Mock Google API key for testing."""
    monkeypatch.setenv("GOOGLE_API_KEY", "test-google-key")
    yield
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)


@pytest.fixture
def clean_env(monkeypatch):
    """Clean environment variables for testing."""
    # Remove API keys if they exist
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    yield


@pytest.fixture
def sample_markdown_content():
    """Sample markdown content for testing."""
    return """# Test Document

This is a test document for DocRAG Kit.

## Section 1

Content for section 1.

## Section 2

Content for section 2 with some **bold** and *italic* text.

### Subsection 2.1

More detailed content here.

```python
def hello():
    print("Hello, World!")
```

## Section 3

Final section with a list:

- Item 1
- Item 2
- Item 3
"""


@pytest.fixture
def sample_config_dict():
    """Sample configuration dictionary for testing."""
    return {
        "project": {
            "name": "Test Project",
            "type": "general"
        },
        "llm": {
            "provider": "openai",
            "embedding_model": "text-embedding-3-small",
            "llm_model": "gpt-4o-mini",
            "temperature": 0.3
        },
        "indexing": {
            "directories": ["."],
            "extensions": [".md", ".txt"],
            "exclude_patterns": ["node_modules/", ".git/", "__pycache__/"]
        },
        "chunking": {
            "chunk_size": 800,
            "chunk_overlap": 150
        },
        "retrieval": {
            "top_k": 3
        },
        "prompt": {
            "template": "Context: {context}\nQuestion: {question}\nAnswer:"
        }
    }
