# Product Overview

DocRAG Kit is a universal RAG (Retrieval-Augmented Generation) system for project documentation. It enables AI-powered semantic search over any project's documentation through a simple CLI interface.

## Core Purpose

Quickly add intelligent documentation search to any project by:
- Indexing documentation files (Markdown, code, configs)
- Creating vector embeddings using OpenAI or Google Gemini
- Providing semantic search via Model Context Protocol (MCP) integration with Kiro AI

## Key Features

- **Quick Setup**: Single command initialization with interactive wizard
- **Universal**: Works with any documentation format
- **MCP Integration**: Seamless integration with Kiro AI assistant
- **Multilingual**: Supports Russian and English
- **Project Templates**: Predefined templates for Symfony, iOS, and general projects
- **Secure**: API keys stored in .env files, never committed

## Target Users

Developers who want to enable AI assistants to understand and answer questions about their project documentation without manual context switching.

## Primary Workflow

1. `docrag init` - Initialize RAG system in project
2. `docrag index` - Index documentation and create vector database
3. `docrag mcp-config` - Get MCP configuration for Kiro
4. Ask questions through Kiro AI about the project

## MCP Tools Provided

- `search_docs`: Fast semantic search returning document fragments (no LLM, ~1s)
- `answer_question`: AI-generated comprehensive answers (uses LLM, ~3-5s)
- `list_indexed_docs`: List all indexed source files
