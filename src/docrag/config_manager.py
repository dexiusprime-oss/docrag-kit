"""Configuration management for DocRAG Kit."""

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml
import os


@dataclass
class ProjectConfig:
    """Project configuration."""
    name: str
    type: str  # symfony, ios, general, custom


@dataclass
class LLMConfig:
    """LLM provider configuration."""
    provider: str  # openai, gemini
    embedding_model: str
    llm_model: str
    temperature: float = 0.3


@dataclass
class IndexingConfig:
    """Document indexing configuration."""
    directories: List[str]
    extensions: List[str]
    exclude_patterns: List[str]


@dataclass
class ChunkingConfig:
    """Document chunking configuration."""
    chunk_size: int = 800  # Optimized for faster processing
    chunk_overlap: int = 150  # Optimized overlap


@dataclass
class RetrievalConfig:
    """Retrieval configuration."""
    top_k: int = 3  # Reduced from 5 for faster response


@dataclass
class PromptConfig:
    """Prompt template configuration."""
    template: str


@dataclass
class DocRAGConfig:
    """Complete DocRAG configuration container."""
    project: ProjectConfig
    llm: LLMConfig
    indexing: IndexingConfig
    chunking: ChunkingConfig
    retrieval: RetrievalConfig
    prompt: PromptConfig

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'project': asdict(self.project),
            'llm': asdict(self.llm),
            'indexing': asdict(self.indexing),
            'chunking': asdict(self.chunking),
            'retrieval': asdict(self.retrieval),
            'prompt': asdict(self.prompt)
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocRAGConfig':
        """Create configuration from dictionary."""
        return cls(
            project=ProjectConfig(**data['project']),
            llm=LLMConfig(**data['llm']),
            indexing=IndexingConfig(**data['indexing']),
            chunking=ChunkingConfig(**data['chunking']),
            retrieval=RetrievalConfig(**data['retrieval']),
            prompt=PromptConfig(**data['prompt'])
        )


class ConfigManager:
    """Manages DocRAG configuration."""

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize configuration manager.
        
        Args:
            project_root: Root directory of the project. Defaults to current directory.
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.docrag_dir = self.project_root / ".docrag"
        self.config_path = self.docrag_dir / "config.yaml"
        self.env_path = self.project_root / ".env"

    def load_config(self) -> Optional[DocRAGConfig]:
        """
        Load configuration from YAML file.
        
        Returns:
            DocRAGConfig object if file exists, None otherwise.
        
        Raises:
            yaml.YAMLError: If YAML parsing fails.
            KeyError: If required configuration fields are missing.
        """
        if not self.config_path.exists():
            return None
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not data:
                return None
            
            return DocRAGConfig.from_dict(data)
        
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Failed to parse config.yaml: {e}")
        except KeyError as e:
            raise KeyError(f"Missing required configuration field: {e}")

    def save_config(self, config: DocRAGConfig) -> None:
        """
        Save configuration to YAML file.
        
        Args:
            config: DocRAGConfig object to save.
        
        Raises:
            OSError: If file cannot be written.
        """
        # Ensure .docrag directory exists
        self.docrag_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert config to dictionary
        config_dict = config.to_dict()
        
        # Write to YAML file
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        except OSError as e:
            raise OSError(f"Failed to write config.yaml: {e}")

    def validate_config(self, config: DocRAGConfig) -> List[str]:
        """
        Validate configuration parameters.
        
        Args:
            config: DocRAGConfig object to validate.
        
        Returns:
            List of validation error messages. Empty list if valid.
        """
        errors = []
        
        # Validate chunk_size range
        if config.chunking.chunk_size < 100:
            errors.append("chunk_size must be at least 100 characters")
        if config.chunking.chunk_size > 5000:
            errors.append("chunk_size must not exceed 5000 characters")
        
        # Validate top_k
        if config.retrieval.top_k < 1:
            errors.append("top_k must be at least 1")
        
        # Validate provider
        valid_providers = ['openai', 'gemini']
        if config.llm.provider not in valid_providers:
            errors.append(f"provider must be one of: {', '.join(valid_providers)}")
        
        # Validate required fields are present
        if not config.project.name:
            errors.append("project.name is required")
        if not config.project.type:
            errors.append("project.type is required")
        if not config.llm.embedding_model:
            errors.append("llm.embedding_model is required")
        if not config.llm.llm_model:
            errors.append("llm.llm_model is required")
        if not config.indexing.directories:
            errors.append("indexing.directories must contain at least one directory")
        if not config.indexing.extensions:
            errors.append("indexing.extensions must contain at least one extension")
        if not config.prompt.template:
            errors.append("prompt.template is required")
        
        return errors

    def interactive_setup(self) -> DocRAGConfig:
        """
        Run interactive configuration wizard.
        
        Returns:
            DocRAGConfig object with user-provided values.
        """
        print("🚀 DocRAG Kit - Interactive Setup\n")
        
        # Project configuration
        print("📦 Project Configuration")
        project_name = input("Project name: ").strip() or self.project_root.name
        
        print("\nProject type:")
        print("  1. Symfony (PHP framework)")
        print("  2. iOS (Swift/UIKit/SwiftUI)")
        print("  3. General Documentation")
        print("  4. Custom")
        project_type_choice = input("Choose [1-4]: ").strip()
        project_type_map = {
            '1': 'symfony',
            '2': 'ios',
            '3': 'general',
            '4': 'custom'
        }
        project_type = project_type_map.get(project_type_choice, 'general')
        
        # LLM configuration
        print("\n🤖 LLM Provider Configuration")
        print("  1. OpenAI (GPT-4)")
        print("  2. Google Gemini")
        provider_choice = input("Choose provider [1-2]: ").strip()
        provider = 'openai' if provider_choice == '1' else 'gemini'
        
        api_key = input(f"Enter {provider.upper()} API key: ").strip()
        
        # Set default models based on provider
        if provider == 'openai':
            embedding_model = 'text-embedding-3-small'
            llm_model = 'gpt-4o-mini'
        else:
            embedding_model = 'models/embedding-001'
            llm_model = 'gemini-1.5-flash'
        
        # Indexing configuration
        print("\n📁 Indexing Configuration")
        print("Suggested directories: docs/, README.md, src/")
        dirs_input = input("Directories to index (comma-separated) [docs/,README.md]: ").strip()
        directories = [d.strip() for d in dirs_input.split(',')] if dirs_input else ['docs/', 'README.md']
        
        print("\nSuggested extensions: .md, .txt, .py, .php, .swift, .json, .yaml")
        exts_input = input("File extensions (comma-separated) [.md,.txt]: ").strip()
        extensions = [e.strip() for e in exts_input.split(',')] if exts_input else ['.md', '.txt']
        
        print("\nSuggested exclusions: node_modules/, .git/, __pycache__/, vendor/")
        excl_input = input("Exclusion patterns (comma-separated) [node_modules/,.git/,__pycache__/]: ").strip()
        exclude_patterns = [p.strip() for p in excl_input.split(',')] if excl_input else ['node_modules/', '.git/', '__pycache__/']
        
        # GitHub token (optional)
        print("\n🔑 GitHub Integration (Optional)")
        github_token_input = input("GitHub Personal Access Token (press Enter to skip): ").strip()
        github_token = github_token_input if github_token_input else None
        
        # Get prompt template based on project type
        from .prompt_templates import PromptTemplateManager
        prompt_template = PromptTemplateManager.get_template(project_type)
        
        # Create configuration
        config = DocRAGConfig(
            project=ProjectConfig(name=project_name, type=project_type),
            llm=LLMConfig(
                provider=provider,
                embedding_model=embedding_model,
                llm_model=llm_model,
                temperature=0.3
            ),
            indexing=IndexingConfig(
                directories=directories,
                extensions=extensions,
                exclude_patterns=exclude_patterns
            ),
            chunking=ChunkingConfig(chunk_size=800, chunk_overlap=150),  # Smaller chunks for faster processing
            retrieval=RetrievalConfig(top_k=3),  # Fewer docs for faster response
            prompt=PromptConfig(template=prompt_template)
        )
        
        # Save API key and GitHub token to .env
        self._save_env_vars(provider, api_key, github_token)
        
        return config

    def _save_env_vars(self, provider: str, api_key: str, github_token: Optional[str] = None) -> None:
        """
        Save API keys and tokens to .env file.
        
        Args:
            provider: LLM provider name (openai or gemini).
            api_key: API key for the provider.
            github_token: Optional GitHub Personal Access Token.
        """
        # Read existing .env content if it exists
        existing_content = ""
        if self.env_path.exists():
            with open(self.env_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        
        # Prepare new content to append
        new_lines = []
        
        # Add API key
        if provider == 'openai':
            key_name = 'OPENAI_API_KEY'
        else:
            key_name = 'GOOGLE_API_KEY'
        
        # Check if key already exists
        if key_name not in existing_content:
            new_lines.append(f"{key_name}={api_key}")
        
        # Add GitHub token if provided
        if github_token and 'GITHUB_TOKEN' not in existing_content:
            new_lines.append(f"GITHUB_TOKEN={github_token}")
        
        # Append new content if there's anything to add
        if new_lines:
            with open(self.env_path, 'a', encoding='utf-8') as f:
                if existing_content and not existing_content.endswith('\n'):
                    f.write('\n')
                f.write('\n'.join(new_lines) + '\n')
