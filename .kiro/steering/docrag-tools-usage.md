---
inclusion: manual
---

# DocRAG Tools Usage Guide for Agents

This guide helps AI agents effectively use DocRAG MCP tools in this project.

## Available Tools

### 1. `search_docs` - Fast Fragment Search

**Purpose**: Quick semantic search returning raw document fragments

**When to use**:
- Need to find specific documentation sections quickly
- Want to read exact documentation text
- Looking for code examples or configuration snippets
- Need multiple relevant fragments to analyze

**Parameters**:
- `question` (required): Search query or topic
- `max_results` (optional): Number of results (1-10, default: 3)

**Returns**: Document fragments with source files and content previews

**Example**:
```
search_docs(question="How to configure database connection?", max_results=3)
```

**Output format**:
```
🔍 Found 3 relevant document(s):

--- Result 1 ---
📄 Source: docs/configuration.md

Database configuration is stored in .env file:
DB_HOST=localhost
DB_PORT=5432
...

--- Result 2 ---
📄 Source: README.md
...
```

### 2. `answer_question` - AI-Generated Answer

**Purpose**: Get comprehensive AI-generated answer synthesized from documentation

**When to use**:
- Need a direct answer to a complex question
- Question requires synthesis from multiple sources
- Want explanation with context
- Need source attribution

**Parameters**:
- `question` (required): Question to answer
- `include_sources` (optional): Include source files (default: true)

**Returns**: AI-generated answer with optional source attribution

**Example**:
```
answer_question(question="What is the deployment process for this project?")
```

**Output format**:
```
The deployment process consists of three main steps:

1. Build the application using `npm run build`
2. Run tests with `npm test`
3. Deploy to production using `./deploy.sh`

Sources:
  • docs/DEPLOYMENT.md
  • README.md
```

### 3. `list_indexed_docs` - List Available Documentation

**Purpose**: See all indexed documentation files

**When to use**:
- Want to know what documentation is available
- Verifying indexing worked correctly
- Need to understand documentation structure

**Parameters**: None

**Returns**: List of all indexed files

**Example**:
```
list_indexed_docs()
```

## Decision Tree for Tool Selection

```
Question about project documentation?
│
├─ Need quick access to specific sections?
│  └─ Use: search_docs
│     - Fast, no LLM processing
│     - Returns raw fragments
│     - Good for finding exact text
│
├─ Need comprehensive answer?
│  └─ Use: answer_question
│     - Synthesizes information
│     - Provides context
│     - Best for complex questions
│
└─ Want to see available docs?
   └─ Use: list_indexed_docs
      - Shows all indexed files
      - No search needed
```

## Best Practices

### 1. Start with `search_docs` for Speed

For most queries, start with `search_docs`:
- Faster (no LLM call)
- Shows exact documentation text
- You can read and interpret yourself

### 2. Use `answer_question` for Complex Queries

Switch to `answer_question` when:
- Question requires synthesis
- Need explanation, not just facts
- Multiple sources need to be combined

### 3. Adjust `max_results` Based on Need

```python
# Quick check - 1 result
search_docs(question="API endpoint", max_results=1)

# Standard search - 3 results (default)
search_docs(question="authentication flow")

# Comprehensive search - 5-10 results
search_docs(question="architecture overview", max_results=7)
```

### 4. Combine Tools for Best Results

**Pattern 1: Search then Answer**
```
1. search_docs(question="deployment") → Get quick overview
2. If not sufficient → answer_question(question="How to deploy?")
```

**Pattern 2: List then Search**
```
1. list_indexed_docs() → See what's available
2. search_docs(question="specific topic") → Find relevant sections
```

## Performance Considerations

### Speed Comparison

| Tool | Speed | LLM Call | Best For |
|------|-------|----------|----------|
| `search_docs` | Fast (~1s) | No | Quick lookups |
| `answer_question` | Slower (~3-5s) | Yes | Complex questions |
| `list_indexed_docs` | Instant | No | Browsing |

### Token Usage

- `search_docs`: No tokens used (vector search only)
- `answer_question`: Uses tokens for LLM generation
- `list_indexed_docs`: No tokens used

**Recommendation**: Use `search_docs` first to save tokens and time.

## Common Patterns

### Pattern 1: Finding Configuration

```python
# Quick: Find config examples
search_docs(question="environment variables", max_results=2)

# Detailed: Explain configuration
answer_question(question="How do I configure the application?")
```

### Pattern 2: Understanding Architecture

```python
# Quick: Find architecture docs
search_docs(question="system architecture", max_results=5)

# Detailed: Get architectural explanation
answer_question(question="Explain the system architecture")
```

### Pattern 3: Troubleshooting

```python
# Quick: Find error messages
search_docs(question="connection timeout error", max_results=3)

# Detailed: Get troubleshooting steps
answer_question(question="How to fix connection timeout errors?")
```

### Pattern 4: Learning API

```python
# Quick: Find API endpoints
search_docs(question="REST API endpoints", max_results=5)

# Detailed: Understand API usage
answer_question(question="How do I use the REST API?")
```

## Error Handling

Both tools return user-friendly error messages:

```
Question cannot be empty
Vector database not found. Run 'docrag index' first.
OpenAI API key not found. Add OPENAI_API_KEY to .env file.
```

If you encounter errors:
1. Check that documentation is indexed (`list_indexed_docs`)
2. Verify API keys are configured
3. Try rephrasing the question
4. Reduce `max_results` if getting too much data

## Examples

### Example 1: Quick Reference Lookup

```python
# Agent needs to find a specific command
result = search_docs(
    question="docker compose command",
    max_results=2
)
# Returns: Exact commands from documentation
```

### Example 2: Understanding Workflow

```python
# Agent needs to understand a process
result = answer_question(
    question="What is the testing workflow?",
    include_sources=True
)
# Returns: Synthesized explanation with sources
```

### Example 3: Exploring Documentation

```python
# Agent wants to see what's available
docs = list_indexed_docs()
# Returns: List of all indexed files

# Then search specific topic
result = search_docs(question="authentication", max_results=3)
# Returns: Relevant fragments about authentication
```

## Summary

- **`search_docs`**: Fast, raw fragments, no LLM → Use first
- **`answer_question`**: Slow, synthesized answer, uses LLM → Use for complex questions
- **`list_indexed_docs`**: Instant, shows available docs → Use for discovery

Choose the right tool based on your needs: speed vs comprehensiveness.
