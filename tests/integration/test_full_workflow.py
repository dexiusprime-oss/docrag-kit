"""Integration tests for full DocRAG workflow."""

import pytest
import os
from pathlib import Path
from docrag.config_manager import ConfigManager, DocRAGConfig
from docrag.document_processor import DocumentProcessor


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project directory with sample files."""
    # Create sample documentation files
    readme = tmp_path / "README.md"
    readme.write_text("""# Test Project

This is a test project for DocRAG Kit integration testing.

## Features

- Feature 1: Documentation indexing
- Feature 2: Semantic search
- Feature 3: MCP integration
""")
    
    api_doc = tmp_path / "API.md"
    api_doc.write_text("""# API Documentation

## Endpoints

### GET /api/users
Returns list of users.

### POST /api/users
Creates a new user.
""")
    
    return tmp_path


@pytest.fixture
def test_config(temp_project):
    """Create test configuration."""
    from docrag.config_manager import (
        ProjectConfig, LLMConfig, IndexingConfig,
        ChunkingConfig, RetrievalConfig, PromptConfig
    )
    
    return DocRAGConfig(
        project=ProjectConfig(name="Test Project", type="general"),
        llm=LLMConfig(
            provider="openai",
            embedding_model="text-embedding-3-small",
            llm_model="gpt-4o-mini",
            temperature=0.3
        ),
        indexing=IndexingConfig(
            directories=["."],
            extensions=[".md"],
            exclude_patterns=["node_modules/", ".git/"]
        ),
        chunking=ChunkingConfig(chunk_size=800, chunk_overlap=150),
        retrieval=RetrievalConfig(top_k=3),
        prompt=PromptConfig(template="Context: {context}\nQuestion: {question}\nAnswer:")
    )


class TestConfigWorkflow:
    """Test configuration workflow."""
    
    def test_save_and_load_config(self, temp_project, test_config):
        """Test saving and loading configuration."""
        manager = ConfigManager(temp_project)
        
        # Save configuration
        manager.save_config(test_config)
        
        # Verify file was created
        assert manager.config_path.exists()
        
        # Load configuration
        loaded_config = manager.load_config()
        
        # Verify loaded configuration matches
        assert loaded_config is not None
        assert loaded_config.project.name == test_config.project.name
        assert loaded_config.llm.provider == test_config.llm.provider
        assert loaded_config.chunking.chunk_size == test_config.chunking.chunk_size


class TestDocumentProcessing:
    """Test document processing workflow."""
    
    def test_scan_documents(self, temp_project, test_config):
        """Test scanning documents."""
        # Change to temp_project directory for scanning
        import os
        original_dir = os.getcwd()
        os.chdir(temp_project)
        
        try:
            processor = DocumentProcessor(test_config.to_dict())
            
            # Scan files
            files = processor.scan_files(temp_project)
            
            # Verify files were found
            assert len(files) >= 2
            assert any("README.md" in str(f) for f in files)
            assert any("API.md" in str(f) for f in files)
        finally:
            os.chdir(original_dir)
    
    def test_load_documents(self, temp_project, test_config):
        """Test loading documents."""
        import os
        original_dir = os.getcwd()
        os.chdir(temp_project)
        
        try:
            processor = DocumentProcessor(test_config.to_dict())
            
            # Scan and load files
            files = processor.scan_files(temp_project)
            documents = processor.load_documents(files)
            
            # Verify documents were loaded
            assert len(documents) >= 2
            assert all(hasattr(doc, 'page_content') for doc in documents)
            assert all(hasattr(doc, 'metadata') for doc in documents)
        finally:
            os.chdir(original_dir)
    
    def test_chunk_documents(self, temp_project, test_config):
        """Test chunking documents."""
        import os
        original_dir = os.getcwd()
        os.chdir(temp_project)
        
        try:
            processor = DocumentProcessor(test_config.to_dict())
            
            # Load and chunk documents
            files = processor.scan_files(temp_project)
            documents = processor.load_documents(files)
            chunks = processor.chunk_documents(documents)
            
            # Verify chunks were created
            assert len(chunks) > 0
            assert all(hasattr(chunk, 'page_content') for chunk in chunks)
            
            # Verify chunk sizes are reasonable
            for chunk in chunks:
                assert len(chunk.page_content) <= test_config.chunking.chunk_size * 2
        finally:
            os.chdir(original_dir)


class TestEndToEndWorkflow:
    """Test end-to-end workflow."""
    
    def test_complete_workflow(self, temp_project, test_config):
        """Test complete workflow from config to document processing."""
        import os
        original_dir = os.getcwd()
        os.chdir(temp_project)
        
        try:
            # Step 1: Save configuration
            manager = ConfigManager(temp_project)
            manager.save_config(test_config)
            
            # Step 2: Load configuration
            loaded_config = manager.load_config()
            assert loaded_config is not None
            
            # Step 3: Process documents
            processor = DocumentProcessor(loaded_config.to_dict())
            files = processor.scan_files(temp_project)
            assert len(files) >= 2
            
            documents = processor.load_documents(files)
            assert len(documents) >= 2
            
            chunks = processor.chunk_documents(documents)
            assert len(chunks) > 0
            
            # Verify metadata is preserved
            for chunk in chunks:
                assert 'source' in chunk.metadata or 'source_file' in chunk.metadata
        finally:
            os.chdir(original_dir)
