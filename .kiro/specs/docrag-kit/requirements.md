# Requirements Document

## Introduction

DocRAG Kit - универсальный инструмент для быстрой установки и настройки RAG (Retrieval-Augmented Generation) системы в любом проекте. Позволяет индексировать документацию, код и конфигурационные файлы проекта для последующего семантического поиска через MCP (Model Context Protocol) интерфейс в Kiro AI.

## Glossary

- **DocRAG Kit**: Python пакет для установки RAG системы в проект
- **RAG System**: Retrieval-Augmented Generation - система поиска с использованием векторных embeddings и LLM
- **MCP Server**: Model Context Protocol сервер для интеграции с Kiro AI
- **Vector Database**: ChromaDB база данных для хранения векторных представлений документов
- **Project Root**: Корневая директория проекта пользователя
- **Index**: Процесс создания векторных embeddings из документов
- **Reindex**: Процесс обновления векторной базы данных
- **CLI**: Command Line Interface - интерфейс командной строки
- **LLM Provider**: Провайдер языковой модели (OpenAI или Google Gemini)
- **Prompt Template**: Шаблон системного промпта для LLM

## Requirements

### Requirement 1

**User Story:** Как разработчик, я хочу установить DocRAG Kit через pip, чтобы быстро добавить RAG систему в любой проект

#### Acceptance Criteria

1. WHEN a user runs `pip install docrag-kit` THEN the system SHALL install all required dependencies including LangChain, ChromaDB, and MCP libraries
2. WHEN installation completes THEN the system SHALL provide a `docrag` CLI command available globally
3. WHEN a user runs `docrag --version` THEN the system SHALL display the current version number
4. WHEN a user runs `docrag --help` THEN the system SHALL display all available commands and options
5. WHEN installation fails due to missing dependencies THEN the system SHALL provide clear error messages with installation instructions

### Requirement 2

**User Story:** Как разработчик, я хочу инициализировать RAG систему в моем проекте через интерактивный setup, чтобы быстро настроить все параметры

#### Acceptance Criteria

1. WHEN a user runs `docrag init` in a project directory THEN the system SHALL start an interactive configuration wizard
2. WHEN the wizard starts THEN the system SHALL ask for the LLM provider choice (OpenAI or Gemini)
3. WHEN the user selects a provider THEN the system SHALL prompt for the corresponding API key
4. WHEN the wizard asks for directories to index THEN the system SHALL suggest common directories (docs/, README.md, src/) with ability to add custom paths
5. WHEN the wizard asks for file extensions THEN the system SHALL suggest common extensions (.md, .txt, .py, .php, .swift, .json, .yaml) with ability to add custom extensions
6. WHEN the wizard asks for files to exclude THEN the system SHALL suggest common patterns (node_modules/, .git/, __pycache__/, vendor/) with ability to add custom patterns
7. WHEN the wizard asks for project type THEN the system SHALL offer predefined templates (Symfony, iOS, General Documentation, Custom)
8. WHEN all questions are answered THEN the system SHALL create a `.docrag/` directory in the project root
9. WHEN configuration is complete THEN the system SHALL create `.docrag/config.yaml` with all settings
10. WHEN configuration is complete THEN the system SHALL create `.env` file with API keys if it doesn't exist
11. WHEN `.env` already exists THEN the system SHALL append API keys without overwriting existing content
12. WHEN initialization completes THEN the system SHALL display next steps (run `docrag index`)

### Requirement 3

**User Story:** Как разработчик, я хочу индексировать документы моего проекта одной командой, чтобы быстро создать векторную базу данных

#### Acceptance Criteria

1. WHEN a user runs `docrag index` THEN the system SHALL read configuration from `.docrag/config.yaml`
2. WHEN configuration is missing THEN the system SHALL display error message and suggest running `docrag init`
3. WHEN API key is missing THEN the system SHALL display error message with instructions to add it to `.env`
4. WHEN indexing starts THEN the system SHALL scan all configured directories for matching file extensions
5. WHEN scanning files THEN the system SHALL exclude files matching exclusion patterns
6. WHEN files are found THEN the system SHALL display count of files to be indexed
7. WHEN processing documents THEN the system SHALL split them into chunks according to configured chunk size and overlap
8. WHEN creating embeddings THEN the system SHALL use the configured LLM provider and embedding model
9. WHEN saving to database THEN the system SHALL store vectors in `.docrag/vectordb/` directory
10. WHEN indexing completes THEN the system SHALL display statistics (files processed, chunks created, total characters)
11. WHEN indexing fails THEN the system SHALL display clear error message and preserve existing database if any
12. WHEN vector database already exists THEN the system SHALL ask for confirmation before overwriting

### Requirement 4

**User Story:** Как разработчик, я хочу обновлять индекс вручную после изменения документации, чтобы поддерживать актуальность поиска

#### Acceptance Criteria

1. WHEN a user runs `docrag reindex` THEN the system SHALL perform the same process as `docrag index`
2. WHEN reindexing starts THEN the system SHALL display warning that existing database will be replaced
3. WHEN user confirms THEN the system SHALL delete old database and create new one
4. WHEN user cancels THEN the system SHALL abort without changes
5. WHEN reindexing completes THEN the system SHALL display updated statistics

### Requirement 5

**User Story:** Как разработчик, я хочу использовать MCP сервер для поиска в документации через Kiro AI, чтобы получать ответы на вопросы о проекте

#### Acceptance Criteria

1. WHEN DocRAG Kit is initialized THEN the system SHALL create `.docrag/mcp_server.py` file
2. WHEN MCP server starts THEN the system SHALL load configuration from `.docrag/config.yaml`
3. WHEN MCP server starts THEN the system SHALL connect to vector database in `.docrag/vectordb/`
4. WHEN MCP server is queried THEN the system SHALL provide `search_docs` tool for semantic search
5. WHEN MCP server is queried THEN the system SHALL provide `list_indexed_docs` tool for listing all indexed files
6. WHEN `search_docs` is called with a question THEN the system SHALL retrieve top K relevant chunks from vector database
7. WHEN `search_docs` is called with a question THEN the system SHALL use configured prompt template for the project type
8. WHEN `search_docs` is called with a question THEN the system SHALL generate answer using configured LLM
9. WHEN `search_docs` is called with `include_sources=true` THEN the system SHALL append source file names to the answer
10. WHEN `list_indexed_docs` is called THEN the system SHALL return list of all unique source files in the database
11. WHEN MCP server encounters error THEN the system SHALL return user-friendly error message
12. WHEN vector database is missing THEN the system SHALL return error message suggesting to run `docrag index`

### Requirement 6

**User Story:** Как разработчик, я хочу легко подключить MCP сервер к Kiro AI, чтобы начать использовать поиск в документации

#### Acceptance Criteria

1. WHEN a user runs `docrag mcp-config` THEN the system SHALL display MCP server configuration for Kiro
2. WHEN displaying configuration THEN the system SHALL show JSON snippet to add to `~/.kiro/settings/mcp.json`
3. WHEN displaying configuration THEN the system SHALL include absolute path to `.docrag/mcp_server.py`
4. WHEN displaying configuration THEN the system SHALL include project-specific server name
5. WHEN displaying configuration THEN the system SHALL provide instructions for manual addition
6. WHEN user is on macOS THEN the system SHALL detect Kiro installation and offer to add configuration automatically
7. WHEN automatic addition is confirmed THEN the system SHALL backup existing `mcp.json` before modification
8. WHEN automatic addition is confirmed THEN the system SHALL add new server entry without overwriting existing servers

### Requirement 7

**User Story:** Как разработчик, я хочу использовать предустановленные шаблоны промптов для разных типов проектов, чтобы получать релевантные ответы

#### Acceptance Criteria

1. WHEN project type is "Symfony" THEN the system SHALL use Symfony expert prompt template
2. WHEN project type is "iOS" THEN the system SHALL use iOS development expert prompt template
3. WHEN project type is "General Documentation" THEN the system SHALL use general developer assistant prompt template
4. WHEN project type is "Custom" THEN the system SHALL allow user to provide custom prompt template
5. WHEN using Symfony template THEN the prompt SHALL instruct LLM to be expert in Symfony framework, PHP, and related technologies
6. WHEN using iOS template THEN the prompt SHALL instruct LLM to be expert in Swift, UIKit, SwiftUI, and iOS SDK
7. WHEN using General template THEN the prompt SHALL instruct LLM to be helpful developer assistant
8. WHEN answering questions THEN the system SHALL support both Russian and English languages in questions and answers
9. WHEN answering questions THEN the system SHALL preserve code examples and technical terms in original language
10. WHEN prompt template is stored THEN the system SHALL save it in `.docrag/config.yaml`

### Requirement 8

**User Story:** Как разработчик, я хочу настраивать параметры chunking и retrieval, чтобы оптимизировать качество поиска для моего проекта

#### Acceptance Criteria

1. WHEN configuration is created THEN the system SHALL set default chunk size to 1000 characters
2. WHEN configuration is created THEN the system SHALL set default chunk overlap to 200 characters
3. WHEN configuration is created THEN the system SHALL set default top K results to 5
4. WHEN configuration is created THEN the system SHALL set default LLM temperature to 0.3
5. WHEN user runs `docrag config` THEN the system SHALL display current configuration
6. WHEN user runs `docrag config --edit` THEN the system SHALL open `.docrag/config.yaml` in default editor
7. WHEN user modifies configuration THEN the system SHALL validate values on next command execution
8. WHEN chunk size is less than 100 THEN the system SHALL display warning about too small chunks
9. WHEN chunk size is greater than 5000 THEN the system SHALL display warning about too large chunks
10. WHEN top K is less than 1 THEN the system SHALL display error and use default value

### Requirement 9

**User Story:** Как разработчик, я хочу поддержку различных форматов файлов, чтобы индексировать всю документацию проекта

#### Acceptance Criteria

1. WHEN indexing THEN the system SHALL support Markdown files (.md)
2. WHEN indexing THEN the system SHALL support text files (.txt)
3. WHEN indexing THEN the system SHALL support Python files (.py)
4. WHEN indexing THEN the system SHALL support PHP files (.php)
5. WHEN indexing THEN the system SHALL support Swift files (.swift)
6. WHEN indexing THEN the system SHALL support JSON files (.json)
7. WHEN indexing THEN the system SHALL support YAML files (.yaml, .yml)
8. WHEN indexing THEN the system SHALL support configuration files (.conf, .config, .ini)
9. WHEN processing Markdown THEN the system SHALL use MarkdownTextSplitter for better structure preservation
10. WHEN processing code files THEN the system SHALL use RecursiveCharacterTextSplitter
11. WHEN file encoding is not UTF-8 THEN the system SHALL attempt to detect encoding automatically
12. WHEN file cannot be read THEN the system SHALL log warning and continue with other files

### Requirement 10

**User Story:** Как разработчик, я хочу видеть понятные сообщения об ошибках и статусе операций, чтобы понимать что происходит

#### Acceptance Criteria

1. WHEN any command starts THEN the system SHALL display operation name with emoji indicator
2. WHEN operation is in progress THEN the system SHALL display progress information
3. WHEN operation completes successfully THEN the system SHALL display success message with checkmark emoji
4. WHEN operation fails THEN the system SHALL display error message with cross emoji
5. WHEN displaying errors THEN the system SHALL include specific error reason
6. WHEN displaying errors THEN the system SHALL suggest corrective action
7. WHEN indexing THEN the system SHALL display count of files being processed
8. WHEN creating embeddings THEN the system SHALL display progress for large document sets
9. WHEN configuration is invalid THEN the system SHALL display which parameter is incorrect
10. WHEN API key is invalid THEN the system SHALL display provider-specific instructions to obtain new key

### Requirement 11

**User Story:** Как разработчик, я хочу использовать разные LLM провайдеры, чтобы выбрать оптимальный по цене и качеству

#### Acceptance Criteria

1. WHEN selecting provider THEN the system SHALL support OpenAI
2. WHEN selecting provider THEN the system SHALL support Google Gemini
3. WHEN using OpenAI THEN the system SHALL use `text-embedding-3-small` for embeddings by default
4. WHEN using OpenAI THEN the system SHALL use `gpt-4o-mini` for LLM by default
5. WHEN using Gemini THEN the system SHALL use `models/embedding-001` for embeddings by default
6. WHEN using Gemini THEN the system SHALL use `gemini-1.5-flash` for LLM by default
7. WHEN configuration allows THEN the system SHALL support custom model names
8. WHEN API request fails THEN the system SHALL display provider-specific error message
9. WHEN rate limit is exceeded THEN the system SHALL suggest waiting or upgrading plan
10. WHEN provider is changed THEN the system SHALL require reindexing due to different embedding dimensions

### Requirement 12

**User Story:** Как разработчик, я хочу иметь минимальную структуру файлов в проекте, чтобы не загромождать репозиторий

#### Acceptance Criteria

1. WHEN DocRAG Kit is initialized THEN the system SHALL create only `.docrag/` directory
2. WHEN `.docrag/` is created THEN the system SHALL include `config.yaml` file
3. WHEN `.docrag/` is created THEN the system SHALL include `mcp_server.py` file
4. WHEN `.docrag/` is created THEN the system SHALL include `vectordb/` subdirectory
5. WHEN `.docrag/` is created THEN the system SHALL include `.gitignore` file
6. WHEN `.gitignore` is created THEN the system SHALL exclude `vectordb/` from git
7. WHEN `.gitignore` is created THEN the system SHALL exclude `.env` from git
8. WHEN `.gitignore` is created THEN the system SHALL include `config.yaml` in git
9. WHEN `.gitignore` is created THEN the system SHALL include `mcp_server.py` in git
10. WHEN project is cloned THEN the new user SHALL only need to run `docrag index` after adding API key

### Requirement 13

**User Story:** Как разработчик, я хочу видеть документацию и примеры использования, чтобы быстро начать работу

#### Acceptance Criteria

1. WHEN package is installed THEN the system SHALL include README.md with quick start guide
2. WHEN package is installed THEN the system SHALL include EXAMPLES.md with usage examples
3. WHEN user runs `docrag init` for first time THEN the system SHALL display link to documentation
4. WHEN documentation is viewed THEN the system SHALL include installation instructions
5. WHEN documentation is viewed THEN the system SHALL include configuration examples for different project types
6. WHEN documentation is viewed THEN the system SHALL include MCP integration guide
7. WHEN documentation is viewed THEN the system SHALL include troubleshooting section
8. WHEN documentation is viewed THEN the system SHALL include API reference for all CLI commands
9. WHEN examples are viewed THEN the system SHALL include example questions for each project type
10. WHEN examples are viewed THEN the system SHALL include example configurations

### Requirement 14

**User Story:** Как разработчик, я хочу быть уверен, что мои API ключи и токены не попадут в публичный репозиторий, чтобы защитить свои данные

#### Acceptance Criteria

1. WHEN `.docrag/.gitignore` is created THEN the system SHALL include `.env` in exclusion list
2. WHEN `.docrag/.gitignore` is created THEN the system SHALL include `vectordb/` in exclusion list
3. WHEN `.docrag/.gitignore` is created THEN the system SHALL include `*.pyc` and `__pycache__/` in exclusion list
4. WHEN project root `.gitignore` exists THEN the system SHALL check if `.env` is excluded
5. WHEN `.env` is not in root `.gitignore` THEN the system SHALL display warning with instructions to add it
6. WHEN documentation is created THEN the system SHALL include security best practices section
7. WHEN documentation security section is viewed THEN the system SHALL warn about not committing `.env` files
8. WHEN documentation security section is viewed THEN the system SHALL provide instructions for `.env.example` pattern
9. WHEN `docrag init` completes THEN the system SHALL create `.env.example` template without actual keys
10. WHEN `docrag init` completes THEN the system SHALL display security reminder about `.env` file
11. WHEN README.md is created THEN the system SHALL include prominent warning about API key security
12. WHEN user runs `docrag init` THEN the system SHALL verify `.env` is gitignored before proceeding

