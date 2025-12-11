#!/usr/bin/env python3
"""
Fix prompt template in DocRAG configuration.

This script fixes the prompt template to include required {context} and {question} placeholders.
"""

import sys
import yaml
from pathlib import Path


def fix_prompt_template(config_path: Path) -> bool:
    """
    Fix prompt template in configuration file.
    
    Args:
        config_path: Path to config.yaml file
        
    Returns:
        True if fixed successfully, False otherwise
    """
    if not config_path.exists():
        print(f"❌ Configuration file not found: {config_path}")
        return False
    
    try:
        # Load configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Check if prompt template exists
        if 'prompt' not in config or 'template' not in config['prompt']:
            print("❌ No prompt template found in configuration")
            return False
        
        current_template = config['prompt']['template']
        
        # Check if template already has placeholders
        if '{context}' in current_template and '{question}' in current_template:
            print("✅ Prompt template already has required placeholders")
            return True
        
        print("🔧 Fixing prompt template...")
        print(f"\n📋 Current template:")
        print(f"{'=' * 80}")
        print(current_template)
        print(f"{'=' * 80}\n")
        
        # Get project type
        project_type = config.get('project', {}).get('type', 'general')
        
        # Create fixed template based on project type
        if project_type == 'symfony':
            fixed_template = """You are an expert assistant for the {project_name} project - a Symfony-based application.
Answer questions based on the provided documentation context.
Be concise and accurate. Respond in Russian if the question is in Russian.
If you don't know the answer based on the context, say so.

Context:
{context}

Question: {question}

Answer:"""
        elif project_type == 'ios':
            fixed_template = """You are an iOS development expert for the {project_name} project.
Answer questions based on the provided documentation context.
Be concise and accurate. Respond in Russian if the question is in Russian.
If you don't know the answer based on the context, say so.

Context:
{context}

Question: {question}

Answer:"""
        else:  # general
            fixed_template = """You are a developer assistant for the {project_name} project.
Answer questions based on the provided documentation context.
Be concise and accurate. Respond in Russian if the question is in Russian.
If you don't know the answer based on the context, say so.

Context:
{context}

Question: {question}

Answer:"""
        
        # Replace {project_name} with actual project name
        project_name = config.get('project', {}).get('name', 'this')
        fixed_template = fixed_template.replace('{project_name}', project_name)
        
        # Update configuration
        config['prompt']['template'] = fixed_template
        
        # Save configuration
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        print(f"✅ Fixed prompt template:")
        print(f"{'=' * 80}")
        print(fixed_template)
        print(f"{'=' * 80}\n")
        print(f"✅ Configuration saved to {config_path}")
        print("\n📝 Next steps:")
        print("   1. Restart Kiro IDE to reload MCP server")
        print("   2. Try asking a question again")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing prompt template: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    else:
        config_path = Path.cwd() / ".docrag" / "config.yaml"
    
    print(f"🔍 Checking configuration: {config_path}\n")
    
    if fix_prompt_template(config_path):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
