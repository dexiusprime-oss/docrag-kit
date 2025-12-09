# API Reference

## Core Functions

### `search_docs(query: str) -> str`
Search documentation using semantic search.

**Parameters:**
- `query`: The search query string

**Returns:**
- Relevant documentation snippets

### `list_indexed_docs() -> List[str]`
List all indexed documentation files.

**Returns:**
- List of file paths

## Configuration API

### `load_config() -> DocRAGConfig`
Load configuration from `.docrag/config.yaml`.

### `save_config(config: DocRAGConfig) -> None`
Save configuration to disk.
