# Technology Stack

## Language & Runtime

- **Python**: >= 3.10 (required for MCP library)
- **Package Manager**: pip, setuptools
- **Build System**: setuptools with pyproject.toml (PEP 621)

## Core Dependencies

### LLM & Embeddings
- **langchain**: >= 0.1.0 - Core LLM framework
- **langchain-openai**: >= 0.0.5 - OpenAI integration
- **langchain-google-genai**: >= 0.0.5 - Google Gemini integration
- **tiktoken**: >= 0.5.0 - Token counting for OpenAI

### Vector Database
- **chromadb**: >= 0.4.0 - Local vector database
- **langchain-chroma**: >= 0.1.0 - LangChain ChromaDB integration

### CLI & Configuration
- **click**: >= 8.0.0 - CLI framework
- **pyyaml**: >= 6.0 - YAML configuration parsing
- **python-dotenv**: >= 1.0.0 - Environment variable management

### MCP Integration
- **mcp**: >= 0.9.0 - Model Context Protocol for Kiro AI integration

### Utilities
- **chardet**: >= 5.0.0 - Character encoding detection

## Development Dependencies

- **pytest**: >= 7.0.0 - Testing framework
- **pytest-asyncio**: >= 0.21.0 - Async test support
- **hypothesis**: >= 6.0.0 - Property-based testing
- **black**: >= 23.0.0 - Code formatting (line length: 100)
- **flake8**: >= 6.0.0 - Linting
- **mypy**: >= 1.0.0 - Type checking

## Common Commands

### Installation
```bash
# Install from source (development)
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"
```

### CLI Commands
```bash
# Initialize RAG system
docrag init

# Index documentation
docrag index

# Rebuild vector database
docrag reindex

# View configuration
docrag config

# Edit configuration
docrag config --edit

# Get MCP configuration
docrag mcp-config

# Version info
docrag --version
```

### Development Commands
```bash
# Run all tests
pytest

# Run specific test types
pytest tests/unit/
pytest tests/integration/
pytest tests/property/

# Code formatting
black src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
```

### Build & Distribution
```bash
# Build package
python -m build

# Install locally
pip install -e .
```

## Configuration Files

- **pyproject.toml**: Main project configuration (PEP 621 compliant)
- **setup.py**: Backward compatibility wrapper
- **MANIFEST.in**: Package data inclusion rules
- **.gitignore**: Git exclusions

## Code Style

- **Line Length**: 100 characters (Black configuration)
- **Target Python**: 3.10+ (required for MCP library)
- **Type Hints**: Encouraged but not strictly enforced (mypy configured)
- **Docstrings**: Google-style docstrings for public APIs
