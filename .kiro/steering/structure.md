# Project Structure

## Directory Layout

```
docrag-kit/
├── src/docrag/              # Main package source code
├── tests/                   # Test suite
├── .kiro/                   # Kiro AI configuration
├── pyproject.toml           # Project configuration
├── setup.py                 # Build compatibility wrapper
├── README.md                # Main documentation
├── EXAMPLES.md              # Usage examples
├── LICENSE                  # MIT license
└── MANIFEST.in              # Package data manifest
```

## Source Code Organization (`src/docrag/`)

### Core Modules

- **`__init__.py`**: Package initialization, version info, exports
- **`cli.py`**: Click-based CLI commands (init, index, reindex, config, mcp-config)
- **`config_manager.py`**: Configuration management with dataclasses
- **`document_processor.py`**: Document scanning, loading, chunking
- **`vector_db.py`**: ChromaDB vector database operations
- **`mcp_server.py`**: MCP server implementation for Kiro integration
- **`prompt_templates.py`**: Project-specific prompt templates
- **`security.py`**: Security utilities and validation
- **`errors.py`**: Error handling and user feedback
- **`py.typed`**: PEP 561 type marker for type checking support

### Architecture Patterns

**Dataclass-Based Configuration**: All configuration uses Python dataclasses for type safety and validation
- `ProjectConfig`, `LLMConfig`, `IndexingConfig`, `ChunkingConfig`, `RetrievalConfig`, `PromptConfig`
- Centralized in `DocRAGConfig` container class

**Manager Pattern**: Core functionality organized into manager classes
- `ConfigManager`: Handles YAML config loading/saving, interactive setup
- `VectorDBManager`: Manages ChromaDB operations, embeddings, retrieval
- `DocumentProcessor`: Handles file scanning, loading, chunking
- `PromptTemplateManager`: Manages project-specific prompt templates

**LangChain Integration**: Uses LangChain abstractions for LLM operations
- Document loaders and text splitters
- Embeddings (OpenAI, Google Gemini)
- Vector store (ChromaDB)
- Retriever pattern for semantic search

## Test Organization (`tests/`)

```
tests/
├── __init__.py
├── unit/                    # Unit tests for individual modules
├── integration/             # Integration tests for workflows
├── property/                # Property-based tests (Hypothesis)
└── fixtures/                # Shared test fixtures
```

## User Project Structure (After `docrag init`)

When DocRAG Kit is initialized in a user's project:

```
user-project/
├── .docrag/
│   ├── config.yaml          # User configuration
│   ├── mcp_server.py        # Generated MCP server
│   ├── vectordb/            # ChromaDB database (gitignored)
│   └── .gitignore           # Excludes vectordb and .env
├── .env                     # API keys (gitignored)
└── .env.example             # Template without real keys
```

## Key Design Principles

### Separation of Concerns
- CLI layer (`cli.py`) handles user interaction
- Manager classes handle business logic
- LangChain handles LLM operations

### Configuration Management
- YAML for user-facing configuration (`.docrag/config.yaml`)
- `.env` for secrets (API keys)
- Dataclasses for internal representation

### Error Handling
- User-friendly error messages with emoji indicators
- Validation at configuration load time
- Graceful degradation for missing files

### Security
- API keys never in version control
- Automatic `.gitignore` creation
- Security warnings during setup

### Extensibility
- Project templates for different use cases
- Pluggable LLM providers (OpenAI, Gemini)
- Configurable file types and directories

## Module Dependencies

```
cli.py
  └─> config_manager.py
  └─> document_processor.py
  └─> vector_db.py
  └─> prompt_templates.py

config_manager.py
  └─> prompt_templates.py

document_processor.py
  └─> (langchain text splitters)

vector_db.py
  └─> (langchain embeddings, chromadb)

mcp_server.py
  └─> config_manager.py
  └─> vector_db.py
```

## File Naming Conventions

- **Module files**: lowercase with underscores (`vector_db.py`, `config_manager.py`)
- **Class names**: PascalCase (`VectorDBManager`, `ConfigManager`)
- **Functions**: lowercase with underscores (`load_config`, `scan_files`)
- **Constants**: UPPERCASE with underscores (defined in modules as needed)

## Import Organization

Standard Python import order:
1. Standard library imports
2. Third-party imports (langchain, click, etc.)
3. Local module imports (relative imports within package)
