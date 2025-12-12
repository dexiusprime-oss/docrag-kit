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
        print("WARNING: Vector database doesn't exist yet")
        print("   This test requires an existing database")
        # Skip test if no database exists
        return
    
    print("SUCCESS: Vector database exists")
    print(f"   Path: {vectordb_path}")
    
    # Run index command without any input
    # If it prompts, it will hang waiting for input
    print("\nTesting index command (should not prompt)...")
    
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
        assert "Overwrite existing database?" not in output, f"Command is still prompting for confirmation. Output: {output}"
        
        # Check if it mentions overwriting or completes successfully
        success_indicators = [
            "overwriting" in output.lower(),
            "vector database already exists" in output.lower(),
            result.returncode == 0
        ]
        
        assert any(success_indicators), f"Command did not complete successfully. Output: {output}"
        
        print("SUCCESS: Command executed without prompting")
        
    except subprocess.TimeoutExpired:
        assert False, "Command timed out (likely waiting for input)"
    except Exception as e:
        assert False, f"Unexpected error: {e}"

if __name__ == "__main__":
    success = test_index_no_prompt()
    exit(0 if success else 1)
