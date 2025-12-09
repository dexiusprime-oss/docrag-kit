#!/usr/bin/env python3
"""Script to initialize DocRAG Kit configuration programmatically."""

import os
from pathlib import Path
import yaml

# Create .docrag directory
docrag_dir = Path(".docrag")
docrag_dir.mkdir(exist_ok=True)

# Configuration
config = {
    "project": {
        "name": "Test Demo Project",
        "type": "general"
    },
    "llm": {
        "provider": "openai",
        "llm_model": "gpt-4o-mini",
        "embedding_model": "text-embedding-3-small",
        "temperature": 0.3
    },
    "indexing": {
        "directories": ["./"],
        "extensions": [".md", ".txt"],
        "exclude_patterns": [
            ".git/*",
            ".docrag/*",
            "*.pyc",
            "__pycache__/*",
            ".env"
        ]
    },
    "chunking": {
        "chunk_size": 1000,
        "chunk_overlap": 200
    },
    "retrieval": {
        "top_k": 5
    },
    "prompt": {
        "template": """You are a helpful assistant that answers questions about the Test Demo Project based on the provided documentation.

Context from documentation:
{context}

Question: {question}

Please provide a clear and accurate answer based on the documentation above. If the answer is not in the documentation, say so."""
    }
}

# Save configuration
config_path = docrag_dir / "config.yaml"
with open(config_path, 'w') as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)

print(f"✅ Configuration created at {config_path}")

# Create .gitignore
gitignore_path = docrag_dir / ".gitignore"
with open(gitignore_path, 'w') as f:
    f.write("vectordb/\n")
    f.write(".env\n")

print(f"✅ .gitignore created at {gitignore_path}")

# Create .env.example
env_example_path = Path(".env.example")
with open(env_example_path, 'w') as f:
    f.write("# OpenAI API Key\n")
    f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
    f.write("\n")
    f.write("# Google API Key (if using Gemini)\n")
    f.write("# GOOGLE_API_KEY=your_google_api_key_here\n")

print(f"✅ .env.example created at {env_example_path}")

print("\n🎉 DocRAG Kit initialized successfully!")
print("\nNext steps:")
print("  1. Run: docrag index")
print("  2. Run: docrag mcp-config")
print("  3. Add MCP config to Kiro")
