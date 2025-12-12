#!/usr/bin/env python3
"""Test script to debug answer_question functionality."""

import asyncio
import sys
import pytest
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from docrag.mcp_server import MCPServer


@pytest.mark.asyncio
async def test_answer_question():
    """Test the answer_question functionality."""
    
    # Initialize MCP server with test project
    test_project = Path("/Users/paulengel/Documents/medtourchina/com/04")
    
    print(f"🔍 Testing answer_question with project: {test_project}")
    print()
    
    try:
        server = MCPServer(test_project / ".docrag")
        print("✅ MCP Server initialized")
        print()
        
        # Check configuration
        print("📋 Configuration:")
        print(f"  Provider: {server.config.get('llm', {}).get('provider')}")
        print(f"  Model: {server.config.get('llm', {}).get('llm_model')}")
        print(f"  Project type: {server.config.get('project', {}).get('type')}")
        print()
        
        # Check prompt template
        prompt_template = server.config.get('prompt', {}).get('template', '')
        print(f"📝 Prompt template length: {len(prompt_template)} characters")
        if prompt_template:
            print(f"  First 100 chars: {prompt_template[:100]}...")
        else:
            print("  ⚠️  WARNING: Prompt template is EMPTY!")
        print()
        
        # Test question
        question = "Как работает NotificationManager в проекте?"
        print(f"❓ Question: {question}")
        print()
        
        # Call answer_question
        print("🤖 Calling answer_question...")
        result = await server.handle_answer_question(question, include_sources=True)
        
        print("📤 Result:")
        print("=" * 80)
        print(result)
        print("=" * 80)
        print()
        
        # Analyze result
        if "📚 Sources:" in result:
            parts = result.split("📚 Sources:")
            answer_part = parts[0].strip()
            sources_part = parts[1].strip() if len(parts) > 1 else ""
            
            print("📊 Analysis:")
            print(f"  Answer length: {len(answer_part)} characters")
            print(f"  Sources count: {sources_part.count('•')}")
            
            if len(answer_part) < 50:
                print("  ⚠️  WARNING: Answer is very short!")
            else:
                print("  ✅ Answer looks good")
        else:
            print("📊 Analysis:")
            print(f"  Total length: {len(result)} characters")
            if "Sources:" not in result:
                print("  ⚠️  WARNING: No sources section found!")
        
    except Exception as e:
        print(f"ERROR: Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_answer_question())
