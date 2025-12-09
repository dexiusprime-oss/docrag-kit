"""Unit tests for configuration management."""

import pytest
from pathlib import Path
from docrag.config_manager import (
    ConfigManager,
    ProjectConfig,
    LLMConfig,
    IndexingConfig,
    ChunkingConfig,
    RetrievalConfig,
    PromptConfig,
    DocRAGConfig
)


class TestProjectConfig:
    """Test ProjectConfig dataclass."""
    
    def test_create_project_config(self):
        """Test creating project configuration."""
        config = ProjectConfig(name="Test Project", type="general")
        assert config.name == "Test Project"
        assert config.type == "general"
    
    def test_project_config_types(self):
        """Test valid project types."""
        valid_types = ["symfony", "ios", "general", "custom"]
        for ptype in valid_types:
            config = ProjectConfig(name="Test", type=ptype)
            assert config.type == ptype


class TestLLMConfig:
    """Test LLMConfig dataclass."""
    
    def test_create_llm_config_openai(self):
        """Test creating OpenAI LLM configuration."""
        config = LLMConfig(
            provider="openai",
            embedding_model="text-embedding-3-small",
            llm_model="gpt-4o-mini",
            temperature=0.3
        )
        assert config.provider == "openai"
        assert config.embedding_model == "text-embedding-3-small"
        assert config.llm_model == "gpt-4o-mini"
        assert config.temperature == 0.3
    
    def test_create_llm_config_gemini(self):
        """Test creating Gemini LLM configuration."""
        config = LLMConfig(
            provider="gemini",
            embedding_model="models/embedding-001",
            llm_model="gemini-1.5-flash",
            temperature=0.3
        )
        assert config.provider == "gemini"
        assert config.embedding_model == "models/embedding-001"


class TestIndexingConfig:
    """Test IndexingConfig dataclass."""
    
    def test_create_indexing_config(self):
        """Test creating indexing configuration."""
        config = IndexingConfig(
            directories=["."],
            extensions=[".md", ".txt"],
            exclude_patterns=["node_modules/", ".git/"]
        )
        assert "." in config.directories
        assert ".md" in config.extensions
        assert "node_modules/" in config.exclude_patterns


class TestChunkingConfig:
    """Test ChunkingConfig dataclass."""
    
    def test_create_chunking_config(self):
        """Test creating chunking configuration."""
        config = ChunkingConfig(chunk_size=800, chunk_overlap=150)
        assert config.chunk_size == 800
        assert config.chunk_overlap == 150
    
    def test_default_chunking_config(self):
        """Test default chunking configuration."""
        config = ChunkingConfig()
        assert config.chunk_size == 800
        assert config.chunk_overlap == 150


class TestRetrievalConfig:
    """Test RetrievalConfig dataclass."""
    
    def test_create_retrieval_config(self):
        """Test creating retrieval configuration."""
        config = RetrievalConfig(top_k=3)
        assert config.top_k == 3
    
    def test_default_retrieval_config(self):
        """Test default retrieval configuration."""
        config = RetrievalConfig()
        assert config.top_k == 3


class TestPromptConfig:
    """Test PromptConfig dataclass."""
    
    def test_create_prompt_config(self):
        """Test creating prompt configuration."""
        template = "Context: {context}\nQuestion: {question}\nAnswer:"
        config = PromptConfig(template=template)
        assert config.template == template
        assert "{context}" in config.template
        assert "{question}" in config.template


class TestDocRAGConfig:
    """Test complete DocRAG configuration."""
    
    def test_create_complete_config(self):
        """Test creating complete configuration."""
        config = DocRAGConfig(
            project=ProjectConfig(name="Test", type="general"),
            llm=LLMConfig(
                provider="openai",
                embedding_model="text-embedding-3-small",
                llm_model="gpt-4o-mini",
                temperature=0.3
            ),
            indexing=IndexingConfig(
                directories=["."],
                extensions=[".md"],
                exclude_patterns=[]
            ),
            chunking=ChunkingConfig(chunk_size=800, chunk_overlap=150),
            retrieval=RetrievalConfig(top_k=3),
            prompt=PromptConfig(template="Test template")
        )
        
        assert config.project.name == "Test"
        assert config.llm.provider == "openai"
        assert config.chunking.chunk_size == 800
        assert config.retrieval.top_k == 3
    
    def test_config_to_dict(self):
        """Test converting configuration to dictionary."""
        config = DocRAGConfig(
            project=ProjectConfig(name="Test", type="general"),
            llm=LLMConfig(
                provider="openai",
                embedding_model="text-embedding-3-small",
                llm_model="gpt-4o-mini",
                temperature=0.3
            ),
            indexing=IndexingConfig(
                directories=["."],
                extensions=[".md"],
                exclude_patterns=[]
            ),
            chunking=ChunkingConfig(chunk_size=800, chunk_overlap=150),
            retrieval=RetrievalConfig(top_k=3),
            prompt=PromptConfig(template="Test")
        )
        
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        assert "project" in config_dict
        assert "llm" in config_dict
        assert config_dict["project"]["name"] == "Test"
        assert config_dict["llm"]["provider"] == "openai"
    
    def test_config_from_dict(self):
        """Test creating configuration from dictionary."""
        config_dict = {
            "project": {"name": "Test", "type": "general"},
            "llm": {
                "provider": "openai",
                "embedding_model": "text-embedding-3-small",
                "llm_model": "gpt-4o-mini",
                "temperature": 0.3
            },
            "indexing": {
                "directories": ["."],
                "extensions": [".md"],
                "exclude_patterns": []
            },
            "chunking": {"chunk_size": 800, "chunk_overlap": 150},
            "retrieval": {"top_k": 3},
            "prompt": {"template": "Test"}
        }
        
        config = DocRAGConfig.from_dict(config_dict)
        assert config.project.name == "Test"
        assert config.llm.provider == "openai"
        assert config.chunking.chunk_size == 800
    
    def test_config_from_template_general(self):
        """Test creating configuration from general template."""
        config = DocRAGConfig.from_template('general')
        
        assert config.project.name == "My Project"
        assert config.project.type == "general"
        assert config.llm.provider == "openai"
        assert config.llm.embedding_model == "text-embedding-3-small"
        assert config.llm.llm_model == "gpt-4o-mini"
        assert config.llm.temperature == 0.3
        assert config.indexing.directories == ['docs/', 'README.md']
        assert config.indexing.extensions == ['.md', '.txt', '.rst']
        assert config.chunking.chunk_size == 800
        assert config.chunking.chunk_overlap == 150
        assert config.retrieval.top_k == 3
        assert config.prompt.template  # Should have a template
    
    def test_config_from_template_symfony(self):
        """Test creating configuration from symfony template."""
        config = DocRAGConfig.from_template('symfony')
        
        assert config.project.type == "symfony"
        assert config.indexing.directories == ['docs/', 'src/', 'config/']
        assert '.php' in config.indexing.extensions
        assert '.yaml' in config.indexing.extensions
    
    def test_config_from_template_ios(self):
        """Test creating configuration from ios template."""
        config = DocRAGConfig.from_template('ios')
        
        assert config.project.type == "ios"
        assert config.indexing.directories == ['docs/', 'Sources/', 'README.md']
        assert '.swift' in config.indexing.extensions


class TestConfigManager:
    """Test ConfigManager class."""
    
    def test_init_config_manager(self, tmp_path):
        """Test initializing configuration manager."""
        manager = ConfigManager(tmp_path)
        assert manager.project_root == tmp_path
        assert manager.docrag_dir == tmp_path / ".docrag"
        assert manager.config_path == tmp_path / ".docrag" / "config.yaml"
    
    def test_config_manager_default_path(self):
        """Test configuration manager with default path."""
        manager = ConfigManager()
        assert manager.project_root == Path.cwd()
