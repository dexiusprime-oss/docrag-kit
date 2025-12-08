#!/bin/bash
# Test script for DocRAG Kit installation and deployment

set -e

echo "🧪 DocRAG Kit Installation Test"
echo "================================"
echo ""

# Function to get Python version as comparable number
get_python_version() {
    $1 -c 'import sys; print(f"{sys.version_info.major}{sys.version_info.minor:02d}")' 2>/dev/null || echo "0"
}

# Check current Python version
CURRENT_PYTHON="python3"
CURRENT_VERSION=$(get_python_version $CURRENT_PYTHON)
REQUIRED_VERSION=310  # Python 3.10

echo "🔍 Checking Python version..."
echo "   Current: $($CURRENT_PYTHON --version 2>&1)"

if [ "$CURRENT_VERSION" -lt "$REQUIRED_VERSION" ]; then
    echo "⚠️  Python 3.10+ required, but found $($CURRENT_PYTHON --version 2>&1)"
    echo ""
    
    # Check if pyenv is available
    if command -v pyenv &> /dev/null; then
        echo "✅ pyenv found, installing Python 3.10..."
        
        # Install Python 3.10 if not already installed
        if ! pyenv versions | grep -q "3.10"; then
            pyenv install 3.10.14
        fi
        
        # Use Python 3.10 for this session
        export PYENV_VERSION=3.10.14
        CURRENT_PYTHON="python"
        echo "✅ Using Python 3.10 via pyenv"
    else
        echo "❌ pyenv not found. Installing pyenv..."
        echo ""
        
        # Check if Homebrew is available
        if ! command -v brew &> /dev/null; then
            echo "❌ Homebrew not found. Please install Homebrew first:"
            echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
        
        # Install pyenv
        brew install pyenv
        
        # Setup pyenv in current session
        export PYENV_ROOT="$HOME/.pyenv"
        export PATH="$PYENV_ROOT/bin:$PATH"
        eval "$(pyenv init --path)"
        
        # Install Python 3.10
        echo "📥 Installing Python 3.10.14..."
        pyenv install 3.10.14
        export PYENV_VERSION=3.10.14
        CURRENT_PYTHON="python"
        
        echo ""
        echo "✅ Python 3.10 installed via pyenv"
        echo "💡 To use pyenv permanently, add to your ~/.zshrc:"
        echo "   export PYENV_ROOT=\"\$HOME/.pyenv\""
        echo "   export PATH=\"\$PYENV_ROOT/bin:\$PATH\""
        echo "   eval \"\$(pyenv init --path)\""
        echo ""
    fi
else
    echo "✅ Python version OK: $($CURRENT_PYTHON --version 2>&1)"
fi

echo ""

# Create test directory
TEST_DIR="/tmp/docrag-test-$(date +%s)"
echo "📁 Creating test directory: $TEST_DIR"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Create virtual environment
echo "🐍 Creating virtual environment with $CURRENT_PYTHON..."
$CURRENT_PYTHON -m venv venv
source venv/bin/activate

# Upgrade pip first
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

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
