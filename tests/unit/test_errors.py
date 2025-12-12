"""Unit tests for error handling and user feedback."""

import pytest
from docrag.errors import ErrorFormatter, ProgressIndicator, ValidationWarnings


class TestErrorFormatter:
    """Test error message formatting."""
    
    def test_format_error_basic(self):
        """Test basic error formatting."""
        result = ErrorFormatter.format_error(
            "Test Error",
            "Something went wrong",
            "Try again"
        )
        assert "ERROR: Test Error: Something went wrong" in result
        assert "Try again" in result
    
    def test_format_error_with_details(self):
        """Test error formatting with details."""
        result = ErrorFormatter.format_error(
            "Test Error",
            "Something went wrong",
            "Try again",
            "Additional info"
        )
        assert "ERROR: Test Error: Something went wrong" in result
        assert "Try again" in result
        assert "Additional info" in result
    
    def test_format_config_error(self):
        """Test configuration error formatting."""
        result = ErrorFormatter.format_config_error(
            "Invalid YAML",
            "Check your config.yaml syntax"
        )
        assert "ERROR: Configuration Error" in result
        assert "Invalid YAML" in result
        assert "Check your config.yaml syntax" in result
    
    def test_format_api_key_error_openai(self):
        """Test OpenAI API key error formatting."""
        result = ErrorFormatter.format_api_key_error(
            "openai",
            "API key not found"
        )
        assert "ERROR: API Key Error" in result
        assert "API key not found" in result
        assert "OPENAI_API_KEY" in result
        assert "https://platform.openai.com/api-keys" in result
    
    def test_format_api_key_error_gemini(self):
        """Test Gemini API key error formatting."""
        result = ErrorFormatter.format_api_key_error(
            "gemini",
            "Invalid API key"
        )
        assert "ERROR: API Key Error" in result
        assert "Invalid API key" in result
        assert "GOOGLE_API_KEY" in result
        assert "https://makersuite.google.com/app/apikey" in result
    
    def test_get_api_key_instructions_openai(self):
        """Test getting OpenAI API key instructions."""
        result = ErrorFormatter.get_api_key_instructions("openai")
        assert "OpenAI" in result
        assert "https://platform.openai.com/api-keys" in result
        assert "OPENAI_API_KEY" in result
    
    def test_get_api_key_instructions_gemini(self):
        """Test getting Gemini API key instructions."""
        result = ErrorFormatter.get_api_key_instructions("gemini")
        assert "Gemini" in result
        assert "https://makersuite.google.com/app/apikey" in result
        assert "GOOGLE_API_KEY" in result


class TestValidationWarnings:
    """Test validation warnings."""
    
    def test_chunk_size_too_small(self):
        """Test warning for chunk size < 100."""
        warning = ValidationWarnings.check_chunk_size(50)
        assert warning is not None
        assert "too small" in warning.lower() or "слишком маленький" in warning.lower()
    
    def test_chunk_size_too_large(self):
        """Test warning for chunk size > 5000."""
        warning = ValidationWarnings.check_chunk_size(6000)
        assert warning is not None
        assert "too large" in warning.lower() or "слишком большой" in warning.lower()
    
    def test_chunk_size_valid(self):
        """Test no warning for valid chunk size."""
        warning = ValidationWarnings.check_chunk_size(1000)
        assert warning is None
    
    def test_top_k_invalid(self):
        """Test warning for top_k < 1."""
        warning = ValidationWarnings.check_top_k(0)
        assert warning is not None
        assert "top_k" in warning
    
    def test_top_k_valid(self):
        """Test no warning for valid top_k."""
        warning = ValidationWarnings.check_top_k(5)
        assert warning is None
    
    def test_validate_all(self):
        """Test validating all parameters."""
        warnings = ValidationWarnings.validate_all(chunk_size=50, top_k=0)
        assert len(warnings) == 2
        
        warnings = ValidationWarnings.validate_all(chunk_size=1000, top_k=5)
        assert len(warnings) == 0
