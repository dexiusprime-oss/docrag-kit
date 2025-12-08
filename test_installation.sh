#!/bin/bash
# Test script for DocRAG Kit installation and deployment

set -e

echo "🧪 DocRAG Kit Installation Test"
echo "================================"
echo ""

# Create test directory
TEST_DIR="/tmp/docrag-test-$(date +%s)"
echo "📁 Creating test directory: $TEST_DIR"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install from GitHub
echo "📦 Installing docrag-kit from GitHub..."
pip install git+https://github.com/dexiusprime-oss/docrag-kit.git

# Verify installation
echo "✅ Verifying installation..."
docrag --version

# Create test project
echo "📝 Creating test project..."
mkdir test-project
cd test-project

# Create sample documentation
cat > README.md << 'EOF'
# Test Project

This is a test project for DocRAG Kit.

## Features
- Feature 1: Documentation indexing
- Feature 2: Semantic search
- Feature 3: MCP integration
EOF

cat > GUIDE.md << 'EOF'
# User Guide

## Getting Started
Follow these steps to get started with the project.

## Configuration
Configure the system using config files.
EOF

echo "🎯 Test project created with sample docs"
echo ""
echo "📊 Test Results:"
echo "  ✅ Package installed successfully"
echo "  ✅ CLI command available"
echo "  ✅ Test project ready"
echo ""
echo "🎉 Installation test PASSED!"
echo ""
echo "📍 Test location: $TEST_DIR/test-project"
echo ""
echo "Next steps to test manually:"
echo "  1. cd $TEST_DIR/test-project"
echo "  2. source ../venv/bin/activate"
echo "  3. docrag init"
echo "  4. Add your OpenAI API key when prompted"
echo "  5. docrag index"
echo "  6. docrag mcp-config"
