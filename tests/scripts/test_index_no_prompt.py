#!/usr/bin/env python3
"""
Test that docrag index no longer prompts for confirmation.
"""

import subprocess
from pathlib import Path

def test_index_no_prompt():
    """Test that index command doesn't prompt when database exists."""
    
    test_dir = Path("test-demo-project")
    
    # Check if vectordb exists
    vectordb_path = test_dir / ".docrag" / "vectordb"
    
    if not vectordb_path.exists():
        print("⚠️  Vector database doesn't exist yet")
        print("   This test requires an existing database")
        return False
    
    print("✅ Vector database exists")
    print(f"   Path: {vectordb_path}")
    
    # Run index command without any input
    # If it prompts, it will hang waiting for input
    print("\n🧪 Testing index command (should not prompt)...")
    
    try:
        result = subprocess.run(
            ["python3", "-m", "docrag.cli", "index"],
            cwd=test_dir,
            capture_output=True,
            text=True,
            timeout=5,  # Should complete quickly or timeout if waiting for input
            input=""  # No input provided
        )
        
        output = result.stdout + result.stderr
        
        # Check if it's waiting for confirmation
        if "Overwrite existing database?" in output:
            print("❌ FAILED: Command is still prompting for confirmation")
            print(f"\nOutput:\n{output}")
            return False
        
        # Check if it mentions overwriting
        if "overwriting" in output.lower() or "vector database already exists" in output.lower():
            print("✅ PASSED: Command mentions existing database but doesn't prompt")
            print(f"\nOutput snippet:\n{output[:500]}")
            return True
        
        # If no database message, that's also fine (might have been deleted)
        print("✅ PASSED: Command executed without prompting")
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ FAILED: Command timed out (likely waiting for input)")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_index_no_prompt()
    exit(0 if success else 1)
