# Design Document

## Overview

DocRAG Kit is a Python package that provides a turnkey solution for adding RAG (Retrieval-Augmented Generation) capabilities to any project. The system consists of:

1. **CLI Tool** - Command-line interface for setup, indexing, and configuration
2. **MCP Server** - Model Context Protocol server for integration with Kiro AI
3. **Vector Database** - ChromaDB for storing document embeddings
4. **Document Processor** - Pipeline for loading, chunking, and embedding documents
5. **Configuration System** - YAML-based configuration with interactive setup

The design prioritizes simplicity, minimal dependencies, and ease of use while maintaining flexibility for different project types.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Project                          │
│                                                               │
│  ┌────────────┐         ┌──────────────────────────────┐   │
│  │   .docrag/ │         │   Project Files               │   │
│  │            │         │   - docs/                     │   │
│  │  config.yaml◄────────┤   - src/                      │   │
│  │  mcp_server.py       │   - README.md                 │   │
│  │  vectordb/  │        │   - *.php, *.swift, etc.      │   │
│  └─────┬──────┘         └──────────────────────────────┘   │
│        │                                                     │
└────────┼─────────────────────────────────────────────────────┘
         │
         │ reads config
         │
    ┌────▼─────────────────────────────────────────────┐
    │         DocRAG Kit CLI (docrag command)          │
    │                                                   │
    │  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
    │  │   init   │  │  index   │  │ mcp-config   │  │
    │  └──────────┘  └──────────┘  └──────────────┘  │
    └───────────────────┬───────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
    ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
    │ Config  │   │Document │   │  MCP    │
    │ Manager │   │Processor│   │ Server  │
    └─────────┘   └────┬────┘   └────┬────┘
                       │             │
                  ┌────▼────┐   ┌────▼────┐
                  │ChromaDB │   │LangChain│
                  │Vector DB│   │   QA    │
                  └─────────┘   └────┬────┘
                                     │
                            ┌────────▼────────┐
                            │  LLM Provider   │
                            │ (OpenAI/Gemini) │
                            └─────────────────┘
```

### Component Interaction Flow

**Initialization Flow:**
```
User → docrag init → ConfigManager → Interactive Wizard → config.yaml + .env
```

**Indexing Flow:**
```
User → docrag index → ConfigManager → DocumentProcessor → ChromaDB
                                    ↓
                              File Scanner → Chunker → Embeddings → Vector Store
```

**Query Flow (via MCP):**
```
Kiro AI → MCP Server → ConfigManager → ChromaDB Retriever → LangChain QA → LLM → Response
```



## Components and Interfaces

### 1. CLI Tool (`docrag` command)

**Purpose:** Main entry point for all user interactions

**Commands:**
- `docrag init` - Initialize RAG system in current project
- `docrag index` - Index documents and create vector database
- `docrag reindex` - Rebuild vector database from scratch
- `docrag config` - Display current configuration
- `docrag config --edit` - Open configuration file in editor
- `docrag mcp-config` - Display MCP server configuration for Kiro
- `docrag --version` - Display version
- `docrag --help` - Display help

**Implementation:** Python Click library for CLI framework

**Interface:**
```python
@click.group()
def cli():
    """DocRAG Kit - Universal RAG system for projects"""
    pass

@cli.command()
def init():
    """Initialize DocRAG in current project"""
    pass

@cli.command()
def index():
    """Index project documents"""
    pass
```

### 2. Configuration Manager

**Purpose:** Handle all configuration operations

**Responsibilities:**
- Load and validate configuration from `.docrag/config.yaml`
- Interactive wizard for initial setup
- Validate configuration parameters
- Manage environment variables from `.env`

**Configuration Schema:**
```yaml
# .docrag/config.yaml
project:
  name: "my-project"
  type: "symfony"  # symfony, ios, general, custom
  
llm:
  provider: "openai"  # openai, gemini
  embedding_model: "text-embedding-3-small"
  llm_model: "gpt-4o-mini"
  temperature: 0.3

indexing:
  directories:
    - "docs/"
    - "src/"
    - "README.md"
  extensions:
    - ".md"
    - ".txt"
    - ".php"
    - ".py"
  exclude_patterns:
    - "node_modules/"
    - ".git/"
    - "__pycache__/"
    - "vendor/"
  
chunking:
  chunk_size: 1000
  chunk_overlap: 200
  
retrieval:
  top_k: 5

prompt:
  template: |
    You are an expert in {project_type}.
    Use the following context to answer the question.
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:
```

**Interface:**
```python
class ConfigManager:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config_path = project_root / ".docrag" / "config.yaml"
    
    def load_config(self) -> Dict:
        """Load configuration from YAML"""
        pass
    
    def save_config(self, config: Dict):
        """Save configuration to YAML"""
        pass
    
    def validate_config(self, config: Dict) -> bool:
        """Validate configuration parameters"""
        pass
    
    def interactive_setup(self) -> Dict:
        """Run interactive configuration wizard"""
        pass
```

### 3. Document Processor

**Purpose:** Load, process, and chunk documents for indexing

**Responsibilities:**
- Scan directories for matching files
- Load documents with proper encoding detection
- Split documents into chunks
- Add metadata to chunks
- Handle different file types appropriately

**Interface:**
```python
class DocumentProcessor:
    def __init__(self, config: Dict):
        self.config = config
        self.text_splitters = self._init_splitters()
    
    def scan_files(self) -> List[Path]:
        """Scan directories and return list of files to index"""
        pass
    
    def load_documents(self, files: List[Path]) -> List[Document]:
        """Load documents from files"""
        pass
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        pass
    
    def add_metadata(self, chunks: List[Document]) -> List[Document]:
        """Add metadata to chunks"""
        pass
```

**Text Splitters:**
- **MarkdownTextSplitter** - For .md files (preserves structure)
- **RecursiveCharacterTextSplitter** - For code files (.py, .php, .swift)
- **CharacterTextSplitter** - For plain text files

### 4. Vector Database Manager

**Purpose:** Manage ChromaDB vector database operations

**Responsibilities:**
- Initialize ChromaDB client
- Create embeddings using configured provider
- Store vectors with metadata
- Query vectors for retrieval
- Manage database lifecycle (create, delete, update)

**Interface:**
```python
class VectorDBManager:
    def __init__(self, config: Dict):
        self.config = config
        self.db_path = Path(".docrag/vectordb")
        self.embeddings = self._init_embeddings()
    
    def create_database(self, chunks: List[Document]):
        """Create new vector database from chunks"""
        pass
    
    def delete_database(self):
        """Delete existing database"""
        pass
    
    def get_retriever(self, top_k: int):
        """Get retriever for querying"""
        pass
    
    def list_documents(self) -> List[str]:
        """List all indexed documents"""
        pass
```

### 5. MCP Server

**Purpose:** Provide MCP interface for Kiro AI integration

**Responsibilities:**
- Implement MCP protocol
- Expose search_docs and list_indexed_docs tools
- Handle queries and return responses
- Manage LLM chain for answer generation

**Tools:**

**Tool 1: search_docs**
```python
{
    "name": "search_docs",
    "description": "Search project documentation using semantic search",
    "inputSchema": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "Question to search for"
            },
            "include_sources": {
                "type": "boolean",
                "description": "Include source files in response",
                "default": False
            }
        },
        "required": ["question"]
    }
}
```

**Tool 2: list_indexed_docs**
```python
{
    "name": "list_indexed_docs",
    "description": "List all indexed documents in the project",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": []
    }
}
```

**Interface:**
```python
class MCPServer:
    def __init__(self, config_path: Path):
        self.config = ConfigManager(config_path).load_config()
        self.qa_chain = None
    
    def get_qa_chain(self):
        """Lazy load QA chain"""
        pass
    
    async def handle_search_docs(self, question: str, include_sources: bool) -> str:
        """Handle search_docs tool call"""
        pass
    
    async def handle_list_docs(self) -> str:
        """Handle list_indexed_docs tool call"""
        pass
```

### 6. Prompt Template Manager

**Purpose:** Manage prompt templates for different project types

**Predefined Templates:**

**Symfony Template:**
```
You are an expert in Symfony PHP framework and related technologies.
Use the following context from the project documentation to answer the question.

Rules:
- Answer precisely based on the provided context
- If information is not in the context, say so honestly
- Provide code examples when relevant
- Support both Russian and English in questions and answers
- Keep technical terms and code in original language

Context:
{context}

Question: {question}

Answer:
```

**iOS Template:**
```
You are an expert in iOS development with Swift, UIKit, SwiftUI, and iOS SDK.
Use the following context from the project documentation to answer the question.

Rules:
- Answer precisely based on the provided context
- If information is not in the context, say so honestly
- Provide code examples when relevant
- Support both Russian and English in questions and answers
- Keep technical terms and code in original language

Context:
{context}

Question: {question}

Answer:
```

**General Template:**
```
You are a helpful developer assistant.
Use the following context from the project documentation to answer the question.

Rules:
- Answer precisely based on the provided context
- If information is not in the context, say so honestly
- Provide examples when relevant
- Support both Russian and English in questions and answers
- Keep technical terms and code in original language

Context:
{context}

Question: {question}

Answer:
```

**Interface:**
```python
class PromptTemplateManager:
    TEMPLATES = {
        "symfony": SYMFONY_TEMPLATE,
        "ios": IOS_TEMPLATE,
        "general": GENERAL_TEMPLATE
    }
    
    @staticmethod
    def get_template(project_type: str) -> str:
        """Get prompt template for project type"""
        pass
    
    @staticmethod
    def create_custom_template(template: str) -> str:
        """Validate and return custom template"""
        pass
```

## Data Models

### Configuration Model

```python
@dataclass
class ProjectConfig:
    name: str
    type: str  # symfony, ios, general, custom

@dataclass
class LLMConfig:
    provider: str  # openai, gemini
    embedding_model: str
    llm_model: str
    temperature: float

@dataclass
class IndexingConfig:
    directories: List[str]
    extensions: List[str]
    exclude_patterns: List[str]

@dataclass
class ChunkingConfig:
    chunk_size: int
    chunk_overlap: int

@dataclass
class RetrievalConfig:
    top_k: int

@dataclass
class PromptConfig:
    template: str

@dataclass
class DocRAGConfig:
    project: ProjectConfig
    llm: LLMConfig
    indexing: IndexingConfig
    chunking: ChunkingConfig
    retrieval: RetrievalConfig
    prompt: PromptConfig
```

### Document Model

```python
# Using LangChain Document model
from langchain.schema import Document

# Document structure:
{
    "page_content": str,  # Actual text content
    "metadata": {
        "source": str,  # Full file path
        "source_file": str,  # File name only
        "chunk_id": int,  # Chunk index
        "file_type": str,  # File extension
        "project_name": str  # Project name
    }
}
```



## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Configuration persistence
*For any* valid configuration input provided during interactive setup, creating the configuration file and then reading it back should produce equivalent configuration values
**Validates: Requirements 2.10**

### Property 2: Environment file preservation
*For any* existing .env file content, appending API keys should result in a file that contains both the original content and the new API keys
**Validates: Requirements 2.11**

### Property 3: File exclusion correctness
*For any* file path and any exclusion pattern, if the file path matches the exclusion pattern, then the file should not appear in the list of files to be indexed
**Validates: Requirements 3.5**

### Property 4: File count accuracy
*For any* set of discovered files after applying exclusion patterns, the displayed count should equal the actual number of files in the set
**Validates: Requirements 3.6**

### Property 5: Chunk size compliance
*For any* document and any valid chunk size configuration, all generated chunks (except possibly the last one) should have length less than or equal to the configured chunk size
**Validates: Requirements 3.8**

### Property 6: Chunk overlap compliance
*For any* document split into multiple chunks with configured overlap, consecutive chunks should share approximately the configured overlap amount of characters
**Validates: Requirements 3.8**

### Property 7: Top K retrieval correctness
*For any* search query and any configured top K value, the number of returned chunks should be min(K, total_chunks_in_database)
**Validates: Requirements 5.6**

### Property 8: Source inclusion property
*For any* search query with include_sources=true, the response string should contain the substring "Источники:" or "Sources:" followed by file names
**Validates: Requirements 5.9**

### Property 9: Unique documents listing
*For any* vector database state, calling list_indexed_docs should return a list with no duplicate file names
**Validates: Requirements 5.10**

### Property 10: Multilingual support
*For any* question in Russian or English, the system should successfully process it and return a response without language-related errors
**Validates: Requirements 7.8**

### Property 11: Small chunk warning
*For any* chunk size value less than 100, the system should display a warning message containing "too small" or "слишком маленький"
**Validates: Requirements 8.8**

### Property 12: Large chunk warning
*For any* chunk size value greater than 5000, the system should display a warning message containing "too large" or "слишком большой"
**Validates: Requirements 8.9**

### Property 13: Encoding detection fallback
*For any* file with non-UTF-8 encoding that can be detected, the system should successfully load the file content without raising an exception
**Validates: Requirements 9.11**

### Property 14: Graceful file failure
*For any* batch of files where at least one file cannot be read, the system should successfully process all readable files and log warnings for unreadable ones
**Validates: Requirements 9.12**

### Property 15: Error message completeness
*For any* error condition, the error message should be non-empty and contain information about what went wrong
**Validates: Requirements 10.5**

### Property 16: Provider change detection
*For any* configuration where the LLM provider is changed from the previous configuration, the system should detect this change and require reindexing
**Validates: Requirements 11.10**



## Error Handling

### Error Categories

**1. Configuration Errors**
- Missing configuration file → Suggest running `docrag init`
- Invalid YAML syntax → Display line number and syntax error
- Missing required fields → List missing fields
- Invalid parameter values → Display valid ranges/options

**2. API Key Errors**
- Missing API key → Display instructions for adding to .env
- Invalid API key → Display provider-specific error and link to get new key
- Rate limit exceeded → Suggest waiting or upgrading plan
- Network errors → Suggest checking internet connection

**3. File System Errors**
- Permission denied → Display which file/directory and suggest chmod
- Disk full → Display available space and required space
- File not found → Display which file is missing
- Invalid path → Display correct path format

**4. Indexing Errors**
- No files found → Display configured directories and extensions
- Encoding errors → Log warning and continue with other files
- Chunking errors → Display which file failed and why
- Database creation errors → Display ChromaDB error and suggest solutions

**5. MCP Server Errors**
- Database not found → Suggest running `docrag index`
- Query errors → Display error and suggest checking database
- LLM errors → Display provider error message
- Connection errors → Display MCP connection status

### Error Handling Strategy

**Fail Fast:**
- Configuration validation errors
- Missing API keys
- Invalid command arguments

**Fail Gracefully:**
- Individual file processing errors (log and continue)
- Encoding detection failures (try fallback)
- Non-critical warnings (display but continue)

**User-Friendly Messages:**
```python
# Bad
"Error: ENOENT"

# Good
"❌ Configuration file not found: .docrag/config.yaml
   Run 'docrag init' to create configuration"
```

**Error Message Format:**
```
❌ Error: <Short description>
   <Detailed explanation>
   <Suggested action>
```

## Testing Strategy

### Unit Testing

**Test Coverage Areas:**
1. **Configuration Management**
   - YAML parsing and validation
   - Default value assignment
   - Environment variable loading
   - Configuration merging

2. **Document Processing**
   - File scanning with exclusion patterns
   - Document loading with encoding detection
   - Chunking with different splitters
   - Metadata addition

3. **Vector Database Operations**
   - Database creation and deletion
   - Embedding generation
   - Retrieval with different K values
   - Document listing

4. **CLI Commands**
   - Command parsing
   - Argument validation
   - Help text generation
   - Version display

5. **Prompt Templates**
   - Template loading
   - Variable substitution
   - Custom template validation

**Testing Framework:** pytest

**Test Structure:**
```
tests/
├── unit/
│   ├── test_config_manager.py
│   ├── test_document_processor.py
│   ├── test_vector_db_manager.py
│   ├── test_cli.py
│   └── test_prompt_templates.py
├── integration/
│   ├── test_init_flow.py
│   ├── test_index_flow.py
│   └── test_mcp_server.py
└── fixtures/
    ├── sample_docs/
    ├── sample_configs/
    └── sample_env/
```

### Property-Based Testing

**Property Testing Framework:** Hypothesis (Python)

**Test Configuration:**
- Minimum 100 iterations per property
- Use appropriate generators for each data type
- Tag each test with property number from design doc

**Property Test Examples:**

**Property 1: Configuration persistence**
```python
@given(
    project_name=st.text(min_size=1, max_size=50),
    project_type=st.sampled_from(["symfony", "ios", "general"]),
    chunk_size=st.integers(min_value=100, max_value=5000)
)
def test_config_persistence(project_name, project_type, chunk_size):
    """
    Feature: docrag-kit, Property 1: Configuration persistence
    Validates: Requirements 2.10
    """
    config = create_config(project_name, project_type, chunk_size)
    save_config(config)
    loaded_config = load_config()
    assert loaded_config == config
```

**Property 3: File exclusion correctness**
```python
@given(
    file_paths=st.lists(st.text(min_size=1)),
    exclude_pattern=st.text(min_size=1)
)
def test_file_exclusion(file_paths, exclude_pattern):
    """
    Feature: docrag-kit, Property 3: File exclusion correctness
    Validates: Requirements 3.5
    """
    filtered = apply_exclusion(file_paths, exclude_pattern)
    for path in filtered:
        assert not matches_pattern(path, exclude_pattern)
```

**Property 5: Chunk size compliance**
```python
@given(
    document=st.text(min_size=100, max_size=10000),
    chunk_size=st.integers(min_value=100, max_value=2000)
)
def test_chunk_size_compliance(document, chunk_size):
    """
    Feature: docrag-kit, Property 5: Chunk size compliance
    Validates: Requirements 3.8
    """
    chunks = chunk_document(document, chunk_size)
    for chunk in chunks[:-1]:  # All except last
        assert len(chunk) <= chunk_size
```

**Property 7: Top K retrieval correctness**
```python
@given(
    query=st.text(min_size=1),
    k=st.integers(min_value=1, max_value=20)
)
def test_top_k_retrieval(query, k, populated_db):
    """
    Feature: docrag-kit, Property 7: Top K retrieval correctness
    Validates: Requirements 5.6
    """
    results = search_docs(query, k)
    total_docs = count_docs_in_db()
    assert len(results) == min(k, total_docs)
```

**Property 9: Unique documents listing**
```python
@given(
    documents=st.lists(
        st.tuples(st.text(min_size=1), st.text(min_size=1)),
        min_size=1
    )
)
def test_unique_documents_listing(documents):
    """
    Feature: docrag-kit, Property 9: Unique documents listing
    Validates: Requirements 5.10
    """
    # documents is list of (filename, content) tuples
    index_documents(documents)
    listed = list_indexed_docs()
    assert len(listed) == len(set(listed))  # No duplicates
```

**Property 11: Small chunk warning**
```python
@given(chunk_size=st.integers(min_value=1, max_value=99))
def test_small_chunk_warning(chunk_size):
    """
    Feature: docrag-kit, Property 11: Small chunk warning
    Validates: Requirements 8.8
    """
    warnings = validate_chunk_size(chunk_size)
    assert any("too small" in w.lower() or "слишком маленький" in w.lower() 
               for w in warnings)
```

**Property 14: Graceful file failure**
```python
@given(
    readable_files=st.lists(st.text(min_size=1), min_size=1),
    unreadable_count=st.integers(min_value=1, max_value=5)
)
def test_graceful_file_failure(readable_files, unreadable_count, tmp_path):
    """
    Feature: docrag-kit, Property 14: Graceful file failure
    Validates: Requirements 9.12
    """
    # Create readable files
    for content in readable_files:
        create_file(tmp_path, content)
    
    # Create unreadable files
    create_unreadable_files(tmp_path, unreadable_count)
    
    # Process should succeed
    result = process_directory(tmp_path)
    assert result.success
    assert result.processed_count == len(readable_files)
    assert result.failed_count == unreadable_count
```

### Integration Testing

**Test Scenarios:**

1. **Full Initialization Flow**
   - Run `docrag init` with various inputs
   - Verify all files created correctly
   - Verify configuration is valid

2. **Full Indexing Flow**
   - Create test project with sample docs
   - Run `docrag index`
   - Verify vector database created
   - Verify all files indexed

3. **MCP Server Integration**
   - Start MCP server
   - Send search_docs requests
   - Verify responses
   - Send list_indexed_docs requests
   - Verify document list

4. **Provider Switching**
   - Index with OpenAI
   - Switch to Gemini
   - Verify reindex required
   - Reindex with Gemini
   - Verify search works

5. **Error Recovery**
   - Test with missing API key
   - Test with invalid configuration
   - Test with empty project
   - Verify error messages

### Manual Testing Checklist

- [ ] Install via pip in clean environment
- [ ] Run init in new project
- [ ] Test with Symfony project
- [ ] Test with iOS project
- [ ] Test with general docs project
- [ ] Test MCP integration with Kiro
- [ ] Test reindexing
- [ ] Test with OpenAI provider
- [ ] Test with Gemini provider
- [ ] Test error scenarios
- [ ] Test multilingual queries (Russian/English)
- [ ] Verify documentation accuracy



## GitHub Integration (Optional)

### Purpose
Allow users to optionally provide GitHub Personal Access Token for future integrations like automatic repository creation or package publishing.

### Configuration
GitHub token will be stored in `.env` file:
```
GITHUB_TOKEN=ghp_your_token_here
```

### Setup Flow
During `docrag init`, after API key setup:
```
? Do you want to add GitHub token for future integrations? (optional) [y/N]
  If yes:
    ? Enter your GitHub Personal Access Token: 
    → Token saved to .env
    → Instructions displayed for creating token if needed
```

### Token Permissions
Recommended scopes for GitHub token:
- `repo` - Full control of private repositories
- `workflow` - Update GitHub Action workflows

### Future Use Cases
1. **Automatic Repository Creation** - `docrag publish` could create GitHub repo
2. **Package Publishing** - Publish to PyPI with GitHub Actions
3. **Documentation Hosting** - Deploy docs to GitHub Pages
4. **CI/CD Integration** - Setup automated indexing on push

### Security Considerations
- Token stored only in `.env` (gitignored)
- Never logged or displayed in output
- User can skip this step entirely
- Instructions provided for token creation and revocation

## Security and Data Protection

### API Key Protection

**Critical Requirements:**
1. **Never commit API keys to git**
2. **Always use .env files for secrets**
3. **Verify .gitignore before initialization**

### Implementation Strategy

**1. .gitignore Management**
```
.docrag/.gitignore:
  vectordb/
  *.pyc
  __pycache__/
  .env

Root .gitignore (check and warn if missing):
  .env
  .docrag/vectordb/
```

**2. .env.example Pattern**
Create `.env.example` template:
```
# OpenAI API Key (get from https://platform.openai.com/api-keys)
OPENAI_API_KEY=your_openai_key_here

# Google Gemini API Key (get from https://makersuite.google.com/app/apikey)
GOOGLE_API_KEY=your_gemini_key_here

# GitHub Token (optional, for future integrations)
GITHUB_TOKEN=your_github_token_here
```

**3. Pre-initialization Checks**
Before creating `.env`:
- Check if root `.gitignore` exists
- Verify `.env` is in root `.gitignore`
- If not, display warning and instructions
- Offer to add `.env` to root `.gitignore` automatically

**4. Security Warnings**
Display after `docrag init`:
```
✅ Configuration complete!

🔒 SECURITY REMINDER:
   • Your API keys are stored in .env
   • This file is gitignored and will NOT be committed
   • Never share your .env file or commit it to git
   • Use .env.example as a template for other users

📝 Next steps:
   1. Run: docrag index
   2. Run: docrag mcp-config
```

**5. Documentation Security Section**
Include in README.md:
```markdown
## ⚠️ Security Warning

**NEVER commit your `.env` file to git!**

Your `.env` file contains sensitive API keys. Always ensure:
- `.env` is in your `.gitignore`
- You use `.env.example` as a template for sharing
- You never paste API keys in public issues or forums

If you accidentally commit API keys:
1. Revoke them immediately from provider dashboard
2. Generate new keys
3. Update your `.env` file
4. Use `git filter-branch` or BFG Repo-Cleaner to remove from history
```

### Sensitive Data Handling

**What gets gitignored:**
- `.env` - API keys and tokens
- `vectordb/` - Vector database (can be large, regenerated)
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python files

**What gets committed:**
- `config.yaml` - Configuration (no secrets)
- `mcp_server.py` - MCP server code
- `.gitignore` - Exclusion rules
- `.env.example` - Template without real keys

### Error Prevention

**Validation checks:**
```python
def validate_security():
    """Validate security setup before proceeding"""
    
    # Check root .gitignore
    if not root_gitignore_exists():
        warn("No .gitignore found in project root")
        offer_to_create()
    
    # Check .env is excluded
    if not is_env_gitignored():
        error(".env is not in .gitignore!")
        display_instructions()
        return False
    
    return True
```

**Pre-commit hook suggestion:**
```bash
# Suggest adding to .git/hooks/pre-commit
if git diff --cached --name-only | grep -q "^\.env$"; then
    echo "ERROR: Attempting to commit .env file!"
    echo "This file contains sensitive API keys."
    exit 1
fi
```

