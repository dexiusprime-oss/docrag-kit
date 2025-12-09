"""Property-based tests for configuration using Hypothesis."""

import pytest
from hypothesis import given, strategies as st, assume
from docrag.config_manager import (
    ProjectConfig,
    LLMConfig,
    ChunkingConfig,
    RetrievalConfig
)


class TestProjectConfigProperties:
    """Property-based tests for ProjectConfig."""
    
    @given(
        name=st.text(min_size=1, max_size=100),
        project_type=st.sampled_from(["symfony", "ios", "general", "custom"])
    )
    def test_project_config_creation(self, name, project_type):
        """Test ProjectConfig can be created with any valid inputs."""
        config = ProjectConfig(name=name, type=project_type)
        assert config.name == name
        assert config.type == project_type


class TestLLMConfigProperties:
    """Property-based tests for LLMConfig."""
    
    @given(
        provider=st.sampled_from(["openai", "gemini"]),
        temperature=st.floats(min_value=0.0, max_value=2.0, allow_nan=False, allow_infinity=False)
    )
    def test_llm_config_temperature_range(self, provider, temperature):
        """Test LLMConfig accepts valid temperature range."""
        config = LLMConfig(
            provider=provider,
            embedding_model="test-model",
            llm_model="test-llm",
            temperature=temperature
        )
        assert 0.0 <= config.temperature <= 2.0


class TestChunkingConfigProperties:
    """Property-based tests for ChunkingConfig."""
    
    @given(
        chunk_size=st.integers(min_value=100, max_value=5000),
        chunk_overlap=st.integers(min_value=0, max_value=500)
    )
    def test_chunking_config_valid_ranges(self, chunk_size, chunk_overlap):
        """Test ChunkingConfig with valid ranges."""
        # Ensure overlap is less than chunk size
        assume(chunk_overlap < chunk_size)
        
        config = ChunkingConfig(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        assert config.chunk_size >= 100
        assert config.chunk_overlap >= 0
        assert config.chunk_overlap < config.chunk_size
    
    @given(
        chunk_size=st.integers(min_value=100, max_value=5000)
    )
    def test_chunk_overlap_less_than_size(self, chunk_size):
        """Test that chunk overlap is always less than chunk size."""
        chunk_overlap = chunk_size // 4  # 25% overlap
        config = ChunkingConfig(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        assert config.chunk_overlap < config.chunk_size


class TestRetrievalConfigProperties:
    """Property-based tests for RetrievalConfig."""
    
    @given(top_k=st.integers(min_value=1, max_value=20))
    def test_retrieval_config_top_k_range(self, top_k):
        """Test RetrievalConfig with valid top_k range."""
        config = RetrievalConfig(top_k=top_k)
        assert config.top_k >= 1
        assert config.top_k <= 20


class TestConfigInvariants:
    """Test configuration invariants."""
    
    @given(
        chunk_size=st.integers(min_value=100, max_value=5000),
        chunk_overlap=st.integers(min_value=0, max_value=500)
    )
    def test_chunk_overlap_invariant(self, chunk_size, chunk_overlap):
        """Test that chunk overlap is always less than chunk size."""
        assume(chunk_overlap < chunk_size)
        
        config = ChunkingConfig(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        # Invariant: overlap must be less than size
        assert config.chunk_overlap < config.chunk_size
        
        # Invariant: overlap should be reasonable (< 50% of size)
        if config.chunk_overlap > config.chunk_size // 2:
            # This is allowed but not recommended
            pass
    
    @given(
        temperature=st.floats(min_value=0.0, max_value=2.0, allow_nan=False, allow_infinity=False)
    )
    def test_temperature_invariant(self, temperature):
        """Test temperature invariant."""
        config = LLMConfig(
            provider="openai",
            embedding_model="test",
            llm_model="test",
            temperature=temperature
        )
        
        # Invariant: temperature in valid range
        assert 0.0 <= config.temperature <= 2.0
        
        # Invariant: lower temperature = more deterministic
        # Higher temperature = more creative
        if config.temperature < 0.3:
            # Very deterministic
            pass
        elif config.temperature > 1.0:
            # Very creative
            pass
