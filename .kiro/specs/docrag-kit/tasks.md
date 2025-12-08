# Implementation Plan

> **📦 Repository Location:** `/Users/paulengel/Documents/docrag-kit`  
> **📋 Status:** Task 1 completed - Project structure created  
> **📖 Details:** See [REPOSITORY.md](REPOSITORY.md) for repository information



- [x] 1. Setup project structure and packaging
  - Create Python package structure with setup.py/pyproject.toml
  - Configure entry points for CLI command
  - Add dependencies (click, langchain, chromadb, mcp, pyyaml, python-dotenv)
  - Create README.md with installation instructions
  - Create LICENSE file
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 2. Implement Configuration Manager
  - [x] 2.1 Create config data models using dataclasses
    - Define ProjectConfig, LLMConfig, IndexingConfig, ChunkingConfig, RetrievalConfig, PromptConfig
    - Define DocRAGConfig as container for all configs
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 2.2 Implement YAML configuration loading and saving
    - Create load_config() method to read from .docrag/config.yaml
    - Create save_config() method to write to .docrag/config.yaml
    - Handle missing file gracefully
    - _Requirements: 2.9, 2.10_

  - [x] 2.3 Implement configuration validation
    - Validate chunk_size range (100-5000)
    - Validate top_k >= 1
    - Validate provider is openai or gemini
    - Validate required fields are present
    - _Requirements: 8.8, 8.9, 8.10_

  - [ ]* 2.4 Write property test for configuration persistence
    - **Property 1: Configuration persistence**
    - **Validates: Requirements 2.10**

  - [x] 2.5 Implement interactive setup wizard
    - Prompt for LLM provider (openai/gemini)
    - Prompt for API key
    - Prompt for directories to index with suggestions
    - Prompt for file extensions with suggestions
    - Prompt for exclusion patterns with suggestions
    - Prompt for project type (symfony/ios/general/custom)
    - Prompt for GitHub token (optional)
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

  - [x] 2.6 Implement .env file management
    - Create .env if doesn't exist
    - Append API keys without overwriting existing content
    - Add GitHub token if provided
    - _Requirements: 2.10, 2.11_

  - [ ]* 2.7 Write property test for environment file preservation
    - **Property 2: Environment file preservation**
    - **Validates: Requirements 2.11**

- [x] 3. Implement Prompt Template Manager
  - [x] 3.1 Create predefined prompt templates
    - Create Symfony expert template
    - Create iOS expert template
    - Create general documentation template
    - Store templates as constants
    - _Requirements: 7.1, 7.2, 7.3, 7.5, 7.6, 7.7_

  - [x] 3.2 Implement template selection logic
    - get_template() method to retrieve by project type
    - Support for custom templates
    - Template variable validation
    - _Requirements: 7.4, 7.10_

  - [ ]* 3.3 Write unit tests for template manager
    - Test template retrieval for each type
    - Test custom template validation
    - _Requirements: 7.1, 7.2, 7.3_

- [x] 4. Implement Document Processor
  - [x] 4.1 Implement file scanner
    - Scan configured directories recursively
    - Filter by file extensions
    - Apply exclusion patterns
    - Return list of file paths
    - _Requirements: 3.4, 3.5, 3.6_

  - [ ]* 4.2 Write property test for file exclusion
    - **Property 3: File exclusion correctness**
    - **Validates: Requirements 3.5**

  - [ ]* 4.3 Write property test for file count accuracy
    - **Property 4: File count accuracy**
    - **Validates: Requirements 3.6**

  - [x] 4.2 Implement document loader
    - Load files with UTF-8 encoding
    - Detect encoding automatically for non-UTF-8 files
    - Handle encoding errors gracefully
    - Create LangChain Document objects
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.11, 9.12_

  - [ ]* 4.5 Write property test for encoding detection
    - **Property 13: Encoding detection fallback**
    - **Validates: Requirements 9.11**

  - [ ]* 4.6 Write property test for graceful file failure
    - **Property 14: Graceful file failure**
    - **Validates: Requirements 9.12**

  - [x] 4.7 Implement document chunking
    - Initialize MarkdownTextSplitter for .md files
    - Initialize RecursiveCharacterTextSplitter for code files
    - Initialize CharacterTextSplitter for text files
    - Split documents according to chunk_size and chunk_overlap
    - _Requirements: 3.8, 9.9, 9.10_

  - [ ]* 4.8 Write property test for chunk size compliance
    - **Property 5: Chunk size compliance**
    - **Validates: Requirements 3.8**

  - [ ]* 4.9 Write property test for chunk overlap compliance
    - **Property 6: Chunk overlap compliance**
    - **Validates: Requirements 3.8**

  - [x] 4.10 Implement metadata addition
    - Add source file path
    - Add source file name only
    - Add chunk_id
    - Add file_type
    - Add project_name
    - _Requirements: 3.8_

- [x] 5. Implement Vector Database Manager
  - [x] 5.1 Implement embeddings initialization
    - Support OpenAI embeddings (text-embedding-3-small)
    - Support Gemini embeddings (models/embedding-001)
    - Load from configuration
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_

  - [x] 5.2 Implement database creation
    - Initialize ChromaDB client
    - Create embeddings for all chunks
    - Store in .docrag/vectordb/
    - Display progress for large document sets
    - _Requirements: 3.9, 3.10, 10.8_

  - [x] 5.3 Implement database deletion
    - Remove .docrag/vectordb/ directory
    - Handle case when directory doesn't exist
    - _Requirements: 4.3_

  - [x] 5.4 Implement retriever creation
    - Create retriever with configured top_k
    - Return retriever for querying
    - _Requirements: 5.4, 8.3_

  - [ ]* 5.5 Write property test for top K retrieval
    - **Property 7: Top K retrieval correctness**
    - **Validates: Requirements 5.6**

  - [x] 5.6 Implement document listing
    - Query all documents from database
    - Extract unique source file names
    - Return sorted list
    - _Requirements: 5.10_

  - [ ]* 5.7 Write property test for unique documents listing
    - **Property 9: Unique documents listing**
    - **Validates: Requirements 5.10**

  - [x] 5.8 Implement provider change detection
    - Compare current provider with previous config
    - Detect if reindexing is required
    - Display warning message
    - _Requirements: 11.10_

  - [ ]* 5.9 Write property test for provider change detection
    - **Property 16: Provider change detection**
    - **Validates: Requirements 11.10**

- [x] 6. Implement CLI commands
  - [x] 6.1 Create CLI framework with Click
    - Setup main CLI group
    - Add --version flag
    - Add --help flag
    - _Requirements: 1.2, 1.3, 1.4_

  - [x] 6.2 Implement `docrag init` command
    - Check if .docrag/ already exists
    - Run interactive setup wizard
    - Create .docrag/ directory
    - Save configuration to config.yaml
    - Create/update .env file
    - Create .docrag/.gitignore
    - Display next steps
    - _Requirements: 2.1, 2.8, 2.9, 2.10, 2.11, 2.12, 12.1, 12.2, 12.3, 12.5, 12.6, 12.7, 12.8, 12.9_

  - [x] 6.3 Implement `docrag index` command
    - Load configuration
    - Check for API key
    - Scan and load documents
    - Process and chunk documents
    - Create vector database
    - Display statistics
    - Handle confirmation if database exists
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12_

  - [x] 6.4 Implement `docrag reindex` command
    - Display warning about overwriting
    - Ask for confirmation
    - Delete old database
    - Run indexing process
    - Display updated statistics
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 6.5 Implement `docrag config` command
    - Display current configuration
    - Support --edit flag to open in editor
    - _Requirements: 8.6, 8.7_

  - [x] 6.6 Implement `docrag mcp-config` command
    - Generate MCP server configuration JSON
    - Display absolute path to mcp_server.py
    - Show instructions for manual addition
    - Detect Kiro installation on macOS
    - Offer automatic addition if Kiro detected
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_

  - [ ]* 6.7 Write unit tests for CLI commands
    - Test init command flow
    - Test index command flow
    - Test config command
    - Test mcp-config command
    - _Requirements: 1.2, 1.3, 1.4_

- [-] 7. Implement MCP Server
  - [x] 7.1 Create MCP server with mcp library
    - Initialize Server instance
    - Setup stdio transport
    - Implement lazy loading for QA chain
    - _Requirements: 5.1, 5.2, 5.3_

  - [x] 7.2 Implement search_docs tool
    - Define tool schema with question and include_sources parameters
    - Load QA chain with configured LLM and retriever
    - Execute query and get response
    - Optionally append source file names
    - Handle errors gracefully
    - _Requirements: 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.11_

  - [ ]* 7.3 Write property test for source inclusion
    - **Property 8: Source inclusion property**
    - **Validates: Requirements 5.9**

  - [ ]* 7.4 Write property test for multilingual support
    - **Property 10: Multilingual support**
    - **Validates: Requirements 7.8**

  - [x] 7.5 Implement list_indexed_docs tool
    - Define tool schema
    - Query vector database for all documents
    - Extract unique source files
    - Return formatted list
    - Handle empty database
    - _Requirements: 5.5, 5.10, 5.12_

  - [x] 7.6 Implement error handling
    - Handle missing database error
    - Handle API key errors
    - Handle LLM errors
    - Return user-friendly error messages
    - _Requirements: 5.11, 5.12, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

  - [ ]* 7.7 Write property test for error message completeness
    - **Property 15: Error message completeness**
    - **Validates: Requirements 10.5**

  - [ ]* 7.8 Write integration tests for MCP server
    - Test search_docs with various queries
    - Test list_indexed_docs
    - Test error scenarios
    - _Requirements: 5.4, 5.5_

- [x] 8. Implement error handling and user feedback
  - [x] 8.1 Create error message formatter
    - Format with emoji indicators
    - Include error reason
    - Include suggested action
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

  - [x] 8.2 Implement progress indicators
    - Display operation name with emoji
    - Show progress for long operations
    - Display success/failure with appropriate emoji
    - _Requirements: 10.1, 10.7, 10.8_

  - [x] 8.3 Implement validation warnings
    - Warning for chunk_size < 100
    - Warning for chunk_size > 5000
    - Display in user-friendly format
    - _Requirements: 8.8, 8.9_

  - [ ]* 8.4 Write property test for small chunk warning
    - **Property 11: Small chunk warning**
    - **Validates: Requirements 8.8**

  - [ ]* 8.5 Write property test for large chunk warning
    - **Property 12: Large chunk warning**
    - **Validates: Requirements 8.9**

  - [x] 8.6 Implement API key error messages
    - Provider-specific instructions for OpenAI
    - Provider-specific instructions for Gemini
    - Links to get API keys
    - _Requirements: 10.10_

- [x] 9. Create documentation
  - [x] 9.1 Write README.md
    - Installation instructions
    - Quick start guide
    - Basic usage examples
    - Link to full documentation
    - _Requirements: 13.1, 13.4_

  - [x] 9.2 Write EXAMPLES.md
    - Example for Symfony project
    - Example for iOS project
    - Example for general documentation project
    - Example questions for each type
    - Example configurations
    - _Requirements: 13.2, 13.9, 13.10_

  - [x] 9.3 Write MCP integration guide
    - How to get MCP configuration
    - How to add to Kiro manually
    - How to test MCP server
    - Troubleshooting MCP issues
    - _Requirements: 13.6_

  - [x] 9.4 Write troubleshooting guide
    - Common installation issues
    - API key problems
    - Indexing errors
    - MCP connection issues
    - Performance optimization tips
    - _Requirements: 13.7_

  - [x] 9.5 Write API reference
    - Document all CLI commands
    - Document all configuration options
    - Document MCP tools
    - _Requirements: 13.8_

- [x] 10. Implement security and data protection
  - [x] 10.1 Create .gitignore validation
    - Check if root .gitignore exists
    - Verify .env is in root .gitignore
    - Display warning if not gitignored
    - Offer to add .env to root .gitignore
    - _Requirements: 14.4, 14.5, 14.12_

  - [x] 10.2 Create .env.example template
    - Create template with placeholder keys
    - Include comments with links to get keys
    - Include all supported providers
    - _Requirements: 14.8, 14.9_

  - [x] 10.3 Implement security warnings
    - Display security reminder after init
    - Warn about not committing .env
    - Show instructions for .env.example pattern
    - _Requirements: 14.7, 14.10_

  - [x] 10.4 Add security section to documentation
    - Write security best practices
    - Include warning about API keys
    - Provide instructions for accidental commits
    - Add pre-commit hook suggestion
    - _Requirements: 14.6, 14.7, 14.11_

  - [x] 10.5 Create .docrag/.gitignore
    - Exclude vectordb/
    - Exclude .env
    - Exclude *.pyc and __pycache__/
    - _Requirements: 14.1, 14.2, 14.3_

- [x] 11. Setup packaging and distribution
  - [x] 11.1 Configure setup.py or pyproject.toml
    - Set package metadata
    - Define dependencies
    - Configure entry points
    - Set Python version requirement (>=3.8)
    - _Requirements: 1.1, 1.2_

  - [x] 11.2 Create .gitignore for package
    - Exclude __pycache__/
    - Exclude *.pyc
    - Exclude .env
    - Exclude dist/
    - Exclude build/
    - Exclude *.egg-info/
    - _Requirements: 12.6, 12.7_

  - [x] 11.3 Create template .gitignore for projects
    - Exclude vectordb/
    - Exclude .env
    - Include config.yaml
    - Include mcp_server.py
    - _Requirements: 12.6, 12.7, 12.8, 12.9_

  - [x] 11.4 Test package installation
    - Test pip install in clean environment
    - Verify docrag command available
    - Verify all dependencies installed
    - _Requirements: 1.1, 1.2, 1.5_

- [ ] 12. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

